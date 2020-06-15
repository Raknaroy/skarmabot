#   ____  _  __
#  / ___|| |/ /__ _ _ __ _ __ ___   __ _
#  \___ \| ' // _` | '__| '_ ` _ \ / _` |
#   ___) | . \ (_| | |  | | | | | | (_| |
#  |____/|_|\_\__,_|_|  |_| |_| |_|\__,_|
#
# Yet another carma bot for telegram
# Copyright (C) 2020 Nikita Serba. All rights reserved
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

from telegram import Bot
from telegram.error import TimedOut, RetryAfter, Unauthorized

from skarma.karma import KarmaManager
from skarma.utils.errorm import ErrorManager
from skarma.announcements import ChatsManager, AnnouncementsManager


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


def message_handler(update, context):
    km: KarmaManager = KarmaManager()
    chat_id = update.effective_chat.id
    from_user_id = update.effective_user.id
    user_id = update.message.reply_to_message.from_user.id
    user_name = update.message.reply_to_message.from_user.name
    text: str = update.message.text

    if text.startswith('+') or text.startswith('-'):
        if from_user_id == user_id:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Хитрюга!')
            return

        if update.message.reply_to_message.from_user.is_bot:
            context.bot.send_message(chat_id=update.effective_chat.id, text='У роботов нет кармы')
            return

    if text.startswith('+'):
        km.increase_user_karma(chat_id, user_id, 1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'+1 к карме {user_name}\n'
                                      f'Теперь карма {user_name} составляет {km.get_user_karma(chat_id, user_id)}')
    elif text.startswith('-'):
        km.decrease_user_karma(chat_id, user_id, 1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'-1 к карме {user_name}\n'
                                      f'Теперь карма {user_name} составляет {km.get_user_karma(chat_id, user_id)}')


def group_join_handler(update, _):
    chat_id = update.effective_chat.id
    logging.getLogger('botlog').info(f'Group with id #{chat_id} will be added to database after adding bot to it')
    ChatsManager().add_new_chat(chat_id)