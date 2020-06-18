#   ____  _  __
#  / ___|| |/ /__ _ _ __ _ __ ___   __ _
#  \___ \| ' // _` | '__| '_ ` _ \ / _` |
#   ___) | . \ (_| | |  | | | | | | (_| |
#  |____/|_|\_\__,_|_|  |_| |_| |_|\__,_|
#
# Yet another carma bot for telegram
# Copyright (C) 2020 Nikita Serba. All rights reserved
# https://github.com/sandsbit/skarmabot
#
# SKarma is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# SKarma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SKarma. If not, see <https://www.gnu.org/licenses/>.

import time
import logging

from threading import Thread
from enum import Enum

from telegram import Bot
from telegram.error import TimedOut, RetryAfter, Unauthorized

from skarma.karma import KarmaManager, UsernamesManager, StatsManager, MessagesManager
from skarma.utils.errorm import ErrorManager, catch_error
from skarma.utils.db import DBUtils
from skarma.announcements import ChatsManager, AnnouncementsManager
from skarma.commands import hhelp


class AnnouncementsThread(Thread):
    """This thread checks for announcements and send them if there are any"""

    blog = logging.getLogger('botlog')

    chats = []
    last_chats_change_time = -1

    bot: Bot

    def __init__(self, bot: Bot):
        Thread.__init__(self)

        self.blog.info('Creating new announcements thread instance')

        self.change_chats_if_needed()
        self.bot = bot

    def change_chats_if_needed(self) -> bool:
        """
        Reloads chats list from database if it hasn't been reloaded for five minutes

        Returns true if chats was reloaded and false if it five minutes hasn't passed since last reload.
        """
        self.blog.info('Checking if its needed to update chats list')
        current_time = time.time()
        time_change = current_time - self.last_chats_change_time
        if time_change > 5*60:
            self.blog.debug(f"It's been {time_change/60} minutes since last chats list update. Updating...")
            self.chats = ChatsManager().get_all_chats()
            return True
        self.blog.debug("There is no need in updating chats list")
        return False

    def _try_send_message(self, chat_id: int, msg: str):
        i = 0
        while True:
            i += 1

            if i == 10:
                raise TimeoutError('Message sending failed after 10 attempts')

            succ = False
            try:
                self.bot.send_message(chat_id=chat_id, text=msg)
                succ = True
            except TimedOut:
                self.blog.warning('Timout while sending message (we will try one more time): ', exc_info=True)
            except RetryAfter as e:
                self.blog.warning('Telegram send retry_after while sending message (we will try one more time): ',
                                  exc_info=True)
                time.sleep(e.retry_after)
            except Unauthorized:
                self.blog.info(f'Bot was blocked by user with id #{chat_id}')
                ChatsManager().remove_chat(chat_id)
                succ = True
            except Exception as e:
                self.blog.error(e)
                ErrorManager().report_exception(e)
                succ = True

            if succ:
                break

    def run(self) -> None:
        am = AnnouncementsManager()
        while True:
            self.change_chats_if_needed()

            announcements = am.get_all_announcements()

            for id_, msg in announcements:
                self.blog.info(f'Sending new announcement with id ${id_}')
                for chat_id in self.chats:
                    self.blog.debug(f'Sending new announcement with id ${id_} into chat with id #{chat_id}')
                    self._try_send_message(chat_id, msg)
                    time.sleep(2)
                am.delete_announcement(id_)
            time.sleep(10*60)


class ParserResult(Enum):
    NOTHING = 0
    RAISE = 1
    LOWER = 2


RAISE_COMMANDS = [
    '+',
    'плюс',
    'согласен',
    'именно',
    'поддерживаю',
    'красава',
    'лучший',
    'да ты ебаный волшебник',
    'да ты ебаный гений',
    'гениально',
    'совершенно верно',
    'верно',
    'резонно',
    'обьективно',
    'рационально',
    'умно',
    '😍', '👍'
]

LOWER_COMMANDS = [
    '-',
    'ты еблан',
    'долбаеб?',
    'херня',
    'хрень',
    'фигня',
    'хуйня',
    'иди нахуй',
    '🙄', '🖕', '🙅‍', '🤦', '️👎', '😡', '😑', '😐'
]


def _parse_message(msg: str) -> ParserResult:
    """Check if message is karma change command"""
    msg_lower = msg.lower()
    for raise_command in RAISE_COMMANDS:
        if msg_lower.startswith(raise_command):
            return ParserResult.RAISE

    for lower_command in LOWER_COMMANDS:
        if msg_lower.startswith(lower_command):
            return ParserResult.LOWER

    return ParserResult.NOTHING


@catch_error
def message_handler(update, context):
    """Parse message that change someone's karma"""

    km: KarmaManager = KarmaManager()
    chat_id = update.effective_chat.id
    from_user_id = update.effective_user.id
    user_id = update.message.reply_to_message.from_user.id
    user_name = update.message.reply_to_message.from_user.name
    message_id = update.message.reply_to_message.message_id
    text: str = update.message.text

    logging.getLogger('botlog').info(f'Checking reply message from user #{from_user_id} in chat #{chat_id}')

    parse_msg = _parse_message(text)

    if parse_msg != ParserResult.NOTHING:
        unm = UsernamesManager()
        unm.set_username(user_id, user_name)

        if from_user_id == user_id:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Хитрюга!')
            return

        if update.message.reply_to_message.from_user.is_bot:
            context.bot.send_message(chat_id=update.effective_chat.id, text='У роботов нет кармы')
            return

        change_code, change_value = km.check_could_user_change_karma(chat_id, from_user_id,
                                                                     parse_msg == ParserResult.RAISE)

        if change_code == KarmaManager.CHECK.OK:
            if MessagesManager().is_user_changed_karma_on_message(chat_id, from_user_id, message_id):
                context.bot.send_message(chat_id=chat_id, text='Вы уже оценили данное сообщение')
                return
            else:
                MessagesManager().mark_message_as_used(chat_id, from_user_id, message_id)

            StatsManager().handle_user_change_karma(chat_id, from_user_id)

            if parse_msg == ParserResult.RAISE:
                km.increase_user_karma(chat_id, user_id, change_value)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f'+{change_value} к карме {user_name}\n'
                                              f'Теперь карма {user_name} составляет {km.get_user_karma(chat_id, user_id)}')
            else:
                km.decrease_user_karma(chat_id, user_id, change_value)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f'-{change_value} к карме {user_name}\n'
                                              f'Теперь карма {user_name} составляет {km.get_user_karma(chat_id, user_id)}')
        elif change_code == KarmaManager.CHECK.TIMEOUT:
            context.bot.send_message(chat_id=chat_id, text='Вы изменяете карму слишком часто, подождите немного')
        elif change_code == KarmaManager.CHECK.CHANGE_DENIED:
            if parse_msg == ParserResult.RAISE:
                context.bot.send_message(chat_id=chat_id, text='Вы не имеете право увеличивать карму')
            else:
                context.bot.send_message(chat_id=chat_id, text='Вы не имеете право уменьшать карму')
        elif change_code == KarmaManager.CHECK.DAY_MAX_EXCEED:
            context.bot.send_message(chat_id=chat_id, text='Вы исчерпали дневной лимит на изменения кармы')


@catch_error
def handle_group_migration_or_join(update, context):
    for new_member in update.message.new_chat_members:
        if new_member.id == context.bot.id:
            chat_id = update.effective_chat.id
            logging.getLogger('botlog').info(f'Group with id #{chat_id} will be added to database after adding bot to it')
            hhelp(update, context, 'Добро пожаловать!')
            ChatsManager().add_new_chat(chat_id)
    if update.message.migrate_to_chat_id is not None:
        old_chat_id = update.effective_chat.id
        new_chat_id = update.message.migrate_to_chat_id

        logging.getLogger('botlog').info(f'Migrating chat from #{old_chat_id} to #{new_chat_id}')

        db = DBUtils()

        tables = ['chats', 'karma', 'stats']
        for table in tables:
            db.run_single_update_query(f'update {table} set chat_id = %s where chat_id = %s', (new_chat_id, old_chat_id))
