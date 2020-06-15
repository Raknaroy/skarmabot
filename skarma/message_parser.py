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
from telegram.error import TimedOut, RetryAfter

from skarma.karma import KarmaManager
from skarma.announcements import ChatsManager, AnnouncementsManager


class AnnouncementsThread(Thread):
    """This thread checks for announcements and send them if there are any"""

    blog = logging.getLogger('botlog')

    chats = []
    last_chats_change_time = -1

    bot: Bot

    def __init__(self, bot: Bot):
        Thread.__init__(self)

        self.change_chats_if_needed()
        self.bot = bot

    def change_chats_if_needed(self) -> bool:
        """
        Reloads chats list from database if it hasn't been reloaded for five minutes

        Returns true if chats was reloaded and false if it five minutes hasn't passed since last reload.
        """
        current_time = time.time()
        if current_time - self.last_chats_change_time > 5*60:
            self.chats = ChatsManager().get_all_chats()
            return True
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
                pass
            except RetryAfter as e:
                time.sleep(e.retry_after)

            if succ:
                break

    def run(self) -> None:
        am = AnnouncementsManager()
        while True:
            self.change_chats_if_needed()

            announcements = am.get_all_announcements()

            for id_, msg in announcements:
                for chat_id in self.chats:
                    time.sleep(2)
                    self._try_send_message(chat_id, msg)
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
    ChatsManager().add_new_chat(chat_id)