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

from skarma.karma import KarmaManager


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
                                      f'Теперь карма {user_name} состовляет {km.get_user_karma(chat_id, user_id)}')
    elif text.startswith('-'):
        km.decrease_user_karma(chat_id, user_id, 1)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'-1 к карме {user_name}\n'
                                      f'Теперь карма {user_name} состовляет {km.get_user_karma(chat_id, user_id)}')
