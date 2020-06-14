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
from skarma.utils.errorm import ErrorManager


def version(update, context):
    """Send information about bot"""
    logging.getLogger('botlog').info('Printing version info to chat with id ' + str(update.effective_chat.id))

    bot_info = AppInfo()
    message = f"{bot_info.app_name} {bot_info.app_version}\n" \
              f"{bot_info.app_description}\n" \
              f"Build: {bot_info.app_build}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


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


def support(update, context):  # TODO: read links from config file
    """Send information about bot status"""
    logging.getLogger('botlog').info('Printing support info to chat with id ' + str(update.effective_chat.id))

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Вы можете задать свой вопрос или преложить идею для бота по адрессу '
                                  'https://github.com/sandsbit/skarmabot/issues (толькпо по англ.) или '
                                  'же по написв на почту <nikitaserba@icloud.com>.')


def bug_report(update, context):
    """Send information about bot status"""
    logging.getLogger('botlog').info('Printing bug report info to chat with id ' + str(update.effective_chat.id))

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Сообщить об ошибке можно по адрессу https://github.com/sandsbit/skarmabot/issues '
                                  '(толькл по англ.). Используйте эту форму только для сообщения об технических '
                                  'ошибках. Если вас не устраивает что вам/кому-то подняли/опустили карму без повода, '
                                  'обратитесь к администратору группы. Если вы нашли узявимость в боте, сообщите о ней '
                                  'тут: https://github.com/sandsbit/skarmabot/security/advisories/new.')
