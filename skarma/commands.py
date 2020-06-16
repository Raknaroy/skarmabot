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

import logging

from skarma.app_info import AppInfo
from skarma.utils.db import DBUtils
from skarma.utils.errorm import ErrorManager, catch_error
from skarma.karma import KarmaManager, UsernamesManager, NoSuchUser, KarmaRangesManager
from skarma.announcements import ChatsManager


@catch_error
def version(update, context):
    """Send information about bot"""
    logging.getLogger('botlog').info('Printing version info to chat with id ' + str(update.effective_chat.id))

    bot_info = AppInfo()
    message = f"{bot_info.app_name} {bot_info.app_version}\n" \
              f"{bot_info.app_description}\n" \
              f"Build: {bot_info.app_build}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


@catch_error
def status(update, context):
    """Send information about bot status"""
    blog = logging.getLogger('botlog')
    blog.info('Printing status info to chat with id ' + str(update.effective_chat.id))

    number_of_errors = ErrorManager().get_number_of_errors()
    message = f"Status: Running in DEBUG mode ({'Stable' if number_of_errors == 0 else 'Unstable'})\n" \
              f"Unexpected errors: {number_of_errors}\n" \
              f"Logging status: " + ("logging normally\n" if len(blog.handlers) != 0 else "logging init failed\n") + \
              f"Database connection status: " + ("connected" if DBUtils().is_connected() else "disconnected (error)")
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


@catch_error
def support(update, context):  # TODO: read links from config file
    """Send information about bot status"""
    logging.getLogger('botlog').info('Printing support info to chat with id ' + str(update.effective_chat.id))

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Вы можете задать свой вопрос или преложить идею для бота по адрессу '
                                  'https://github.com/sandsbit/skarmabot/issues (толькпо по англ.) или '
                                  'же по написв на почту <nikitaserba@icloud.com>.')


@catch_error
def bug_report(update, context):
    """Send information about bot status"""
    logging.getLogger('botlog').info('Printing bug report info to chat with id ' + str(update.effective_chat.id))

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Сообщить об ошибке можно по адрессу https://github.com/sandsbit/skarmabot/issues '
                                  '(толькл по англ.). Используйте эту форму только для сообщения об технических '
                                  'ошибках. Если вас не устраивает что вам/кому-то подняли/опустили карму без повода, '
                                  'обратитесь к администратору группы. Если вы нашли узявимость в боте, сообщите о ней '
                                  'тут: https://github.com/sandsbit/skarmabot/security/advisories/new.')


@catch_error
def my_karma(update, context):
    """Get user's karma"""
    logging.getLogger('botlog').info(f'Printing karma of user #{update.effective_user.id} '
                                     f'in chat #{update.effective_chat.id}')

    karma = KarmaManager().get_user_karma(update.effective_chat.id, update.effective_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ваша карма: {karma}')


@catch_error
def top(update, context):
    """Print top 5 of chat"""

    chat_id = update.effective_chat.id

    logging.getLogger('botlog').info(f'Printing TOP-5 user in chat #{chat_id}')

    message = 'ТОП-5 людей с лучшей кармой:\n\n'

    top_ = KarmaManager().get_ordered_karma_top(chat_id, 5)
    for user_id, karma in top_:
        try:
            user_name = UsernamesManager().get_username_by_id(user_id)
        except NoSuchUser:
            user_name = f'Unnamed user ({user_id})'
        message += f'{user_name}: {karma}\n'

    context.bot.send_message(chat_id=chat_id, text=message)


@catch_error
def antitop(update, context):
    """Print anti-top 5 of chat"""

    chat_id = update.effective_chat.id

    logging.getLogger('botlog').info(f'Printing TOP-5 user in chat #{chat_id}')

    message = 'ТОП-5 людей с худшей кармой:\n\n'

    top_ = KarmaManager().get_ordered_karma_top(chat_id, 5, biggest=False)
    for user_id, karma in top_:
        try:
            user_name = UsernamesManager().get_username_by_id(user_id)
        except NoSuchUser:
            user_name = f'Unnamed user ({user_id})'
        message += f'{user_name}: {karma}\n'

    context.bot.send_message(chat_id=chat_id, text=message)


admins = [253927284]


@catch_error
def gen_error(update, context):
    """Generate sample error for debugging"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    logging.getLogger('botlog').info(f'Generating sample error! Asked by user #{user_id} in chat #{chat_id}')

    if user_id in admins:
        ErrorManager().report_error('Test error', f'This sample error was generated for debugging '
                                                  f'by user #{user_id} in chat #{chat_id}')
        context.bot.send_message(chat_id=chat_id, text='Sample error successfully generated')
    else:
        logging.getLogger('botlog').debug('Error could bot be generated: access denied. Check admins list')
        context.bot.send_message(chat_id=chat_id, text='Только администратор может сгенерировать тестовую ошибку')


@catch_error
def level(update, context):
    """Send user information about his karma level"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    logging.getLogger('botlog').info(f'Sending karma level info for user #{user_id} in chat #{chat_id}')

    kr = KarmaRangesManager().get_range_by_karma(KarmaManager().get_user_karma(chat_id, user_id))

    message = f'Ваш уровень кармы: {kr.name} ([{kr.min_range}, {kr.max_range}])\n\n'

    if kr.enable_plus:
        message += f'Вы можете прибавлять +{kr.plus_value} едениц(ы/у) кармы\n'
    else:
        message += f'Вы не можете прибавлять карму :(\n'

    if kr.enable_minus:
        message += f'Вы можете отнимать -{kr.minus_value} едениц(ы/у) кармы\n'
    else:
        message += f'Вы не можете прибавлять карму :(\n'

    message += f'Вы можете изменять карму {kr.day_max} раз в день'

    context.bot.send_message(chat_id=chat_id, text=message)


@catch_error
def start(update, _):
    """Save user's chat id"""
    # TODO: help

    chat_id = update.effective_chat.id
    logging.getLogger('botlog').info(f'User with id #{chat_id} will be added to database after running /start')
    ChatsManager().add_new_chat(chat_id)
