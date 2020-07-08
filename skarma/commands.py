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

import logging

from typing import Optional, List, Tuple
from os import path

from skarma.app_info import AppInfo
from skarma.utils.db import DBUtils
from skarma.utils.errorm import ErrorManager, catch_error
from skarma.utils import lang_tools
from skarma.karma import KarmaManager, UsernamesManager, NoSuchUser, KarmaRangesManager
from skarma.announcements import ChatsManager

LICENSE_FILE = "copyinfo.txt"

LICENSE_FILE = path.join(path.dirname(path.abspath(__file__)), '../config', LICENSE_FILE)

license_str: str

with open(LICENSE_FILE, encoding='utf-8') as f:
    license_str = f.read()


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
              f"Unexpected errors: {number_of_errors} (/clear_errors)\n" \
              f"Logging status: " + ("logging normally\n" if len(blog.handlers) != 0 else "logging init failed\n") + \
              f"Database connection status: " + ("connected" if DBUtils().is_connected() else "disconnected (error)")
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


@catch_error
def support(update, context):  # TODO: read links from config file
    """Send information about bot status"""
    logging.getLogger('botlog').info('Printing support info to chat with id ' + str(update.effective_chat.id))

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Вы можете задать свой вопрос или предложить идею для бота по адресу '
                                  'https://github.com/sandsbit/skarmabot/issues (только по англ.) или '
                                  'с помощью специального бота: @skarma_supportbot')


@catch_error
def bug_report(update, context):
    """Send information about bot status"""
    logging.getLogger('botlog').info('Printing bug report info to chat with id ' + str(update.effective_chat.id))

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Сообщить об ошибке можно по адресу https://github.com/sandsbit/skarmabot/issues '
                                  '(толькл по англ.). Используйте эту форму только для сообщения об технических '
                                  'ошибках. Если вас не устраивает что вам/кому-то подняли/опустили карму без повода, '
                                  'обратитесь к администратору группы. Если вы нашли узявимость в боте, ознакомтесь с '
                                  'https://github.com/sandsbit/skarmabot/blob/master/SECURITY.md')


@catch_error
def my_karma(update, context):
    """Get user's karma"""

    if update.effective_chat.type == 'private':
        context.bot.send_message(update.effective_chat.id, text='Эта команда доступна только в групповых чатах!')
        return

    logging.getLogger('botlog').info(f'Printing karma of user #{update.effective_user.id} '
                                     f'in chat #{update.effective_chat.id}')

    karma = KarmaManager().get_user_karma(update.effective_chat.id, update.effective_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ваша карма: {karma}')


def process_top(bd_resp: List[Tuple[int, int]], smile=':(') -> str:
    message = ''

    if len(bd_resp) == 0:
        message += f'В ТОПе никого нет {smile}'

    for user_id, karma in bd_resp:
        try:
            user_name = UsernamesManager().get_username_by_id(user_id)
        except NoSuchUser:
            user_name = f' Unnamed user ({user_id})'
        message += f'{user_name[1:]}: {karma}\n'

    return message


@catch_error
def top(update, context):
    """Print top 5 of chat"""

    if update.effective_chat.type == 'private':
        context.bot.send_message(update.effective_chat.id, text='Эта команда доступна только в групповых чатах!')
        return

    chat_id = update.effective_chat.id

    logging.getLogger('botlog').info(f'Printing TOP-5 user in chat #{chat_id}')

    message = 'ТОП-5 людей с лучшей кармой:\n\n'

    top_ = KarmaManager().get_ordered_karma_top(chat_id, 5)
    message += process_top(top_)

    context.bot.send_message(chat_id=chat_id, text=message)


@catch_error
def antitop(update, context):
    """Print anti-top 5 of chat"""

    if update.effective_chat.type == 'private':
        context.bot.send_message(update.effective_chat.id, text='Эта команда доступна только в групповых чатах!')
        return

    chat_id = update.effective_chat.id

    logging.getLogger('botlog').info(f'Printing TOP-5 user in chat #{chat_id}')

    message = 'ТОП-5 людей с худшей кармой:\n\n'

    top_ = KarmaManager().get_ordered_karma_top(chat_id, 5, biggest=False)
    message += process_top(top_, ':)')

    context.bot.send_message(chat_id=chat_id, text=message)


@catch_error
def gen_error(update, context):
    """Generate sample error for debugging"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    logging.getLogger('botlog').info(f'Generating sample error! Asked by user #{user_id} in chat #{chat_id}')

    if user_id in AppInfo().admins:
        ErrorManager().report_error('Test error', f'This sample error was generated for debugging '
                                                  f'by user #{user_id} in chat #{chat_id}')
        context.bot.send_message(chat_id=chat_id, text='Sample error successfully generated')
    else:
        logging.getLogger('botlog').debug('Error could bot be generated: access denied. Check admins list')
        context.bot.send_message(chat_id=chat_id, text='Только администратор может сгенерировать тестовую ошибку')


def str_find_penultimate(text: str, pattern: str) -> int:
    return text.rfind(pattern, 0, text.rfind(pattern))


@catch_error
def level(update, context):
    """Send user information about his karma level"""

    if update.effective_chat.type == 'private':
        context.bot.send_message(update.effective_chat.id, text='Эта команда доступна только в групповых чатах!')
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    logging.getLogger('botlog').info(f'Sending karma level info for user #{user_id} in chat #{chat_id}')

    kr = KarmaRangesManager().get_range_by_karma(KarmaManager().get_user_karma(chat_id, user_id))

    message = f'Ваш уровень кармы: {kr.name} [{kr.min_range}, {kr.max_range}]\n\n'

    if kr.enable_plus:
        message += f'Вы можете прибавлять ' \
                   f'+{lang_tools.russian_case_nums(kr.plus_value, "еденицу", "еденицы", "едениц")} кармы\n'
    else:
        message += f'Вы не можете прибавлять карму :(\n'

    if kr.enable_minus:
        message += f'Вы можете отнимать ' \
                   f'-{lang_tools.russian_case_nums(kr.minus_value, "еденицу", "еденицы", "едениц")} кармы\n'
    else:
        message += f'Вы не можете отнимать карму :(\n'

    message += f'Вы можете изменять карму {lang_tools.russian_case_nums(int(kr.day_max), "раз", "раза", "раз")}' \
               f' в день и раз в '

    c = 0
    seconds = int(kr.timeout.seconds)
    days = int(kr.timeout.days)
    if days != 0:
        weeks = days // 7
        days_ = days % 7

        if weeks != 0:
            c += 1
            message += lang_tools.russian_case_nums(weeks, 'неделю ', 'недели ', 'недель ')
        if days_ != 0:
            c += 1
            message += lang_tools.russian_case_nums(days_, 'дней ', 'дня ', 'дней ')
    if seconds != 0:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds_ = (seconds % 60)

        if hours != 0:
            c += 1
            message += lang_tools.russian_case_nums(hours, 'час ', 'часа ', 'часов ')
        if minutes != 0:
            c += 1
            message += lang_tools.russian_case_nums(minutes, 'минуту ', 'минуты ', 'минут ')
        if seconds_ != 0:
            c += 1
            message += lang_tools.russian_case_nums(seconds_, 'секунду ', 'секунды ', 'секунд ')

    message = message[:-1]
    lst_spc_i = str_find_penultimate(message, ' ')
    if c > 2:  # yes, >, not >=
        message = message[:lst_spc_i+1] + 'и ' + message[lst_spc_i+1:]

    context.bot.send_message(chat_id=chat_id, text=message)


@catch_error
def hhelp(update, context, custom_first_line: Optional[str] = None):
    chat_id = update.effective_chat.id
    logging.getLogger('botlog').info(f'Sending help to chat #{chat_id}')

    if custom_first_line is not None:
        help_ = custom_first_line + '\n\n'
    else:
        help_ = 'Нужна помощь? Ловите!\n\n'

    help_ += 'Используйте +/- в начале ответа на сообщение, чтобы повысить/понизить ' \
             'карму человека. Бот так же будет реагировать на некоторые фразы, смайлики и стикеры.\n\n' \
             'Карма и ваш чат:\n' \
             '/my_karma - проверить вашу карму\n' \
             '/cancel - отменить последнее действие\n' \
             '/level - узнать уровень вашей кармы\n' \
             '/top - ТОП чата по карме\n' \
             '/antitop - ТОП худших в чате по карме\n' \
             'Про бота: \n' \
             '/help - эта помощь\n' \
             '/version - узнать версию бота\n' \
             '/support - как с нами связаться?\n' \
             '/bug_report - нашли ошибку?\n' \
             '/donate - не дать автору бота умереть от голода\n' \
             'Юридическая хрень: \n' \
             '/license - авторские права и лицензия'
    context.bot.send_message(chat_id=chat_id, text=help_)


@catch_error
def start(update, context):
    """Save user's chat id"""
    hhelp(update, context, 'Добро пожаловать!')

    chat_id = update.effective_chat.id
    logging.getLogger('botlog').info(f'User with id #{chat_id} will be added to database after running /start')
    ChatsManager().add_new_chat(chat_id)


@catch_error
def clear_errors(update, context):
    """Clear all errors in DB"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    logging.getLogger('botlog').info(f'Deleting all errors! Asked by user #{user_id} in chat #{chat_id}')

    if user_id in AppInfo().admins:
        ErrorManager().clear_all_errors()
        context.bot.send_message(chat_id=chat_id, text='All errors successfully deleted')
    else:
        logging.getLogger('botlog').debug('Errors could bot be deleted: access denied. Check admins list')
        context.bot.send_message(chat_id=chat_id, text='Только администратор может удалить все ошибки')


@catch_error
def chat_id_(update, context):
    """Print chat id"""

    chat_id = update.effective_chat.id

    logging.getLogger('botlog').info(f'Printing chat id in chat #{chat_id}')
    context.bot.send_message(chat_id=chat_id, text=f'Current chat id: {chat_id}')


@catch_error
def license_(update, context):
    """Send information about bot status"""
    logging.getLogger('botlog').info('Printing license info to chat with id ' + str(update.effective_chat.id))

    ai = AppInfo()

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'{ai.app_name} {ai.app_version} (build: {ai.app_build})\n\n'
                                  f'{license_str}')
