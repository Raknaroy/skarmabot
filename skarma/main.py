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

import argparse
import logging
import logging.handlers
import os
import sys

from os import path

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from skarma import commands, message_parser
from skarma.app_info import AppInfo
from skarma.utils.errorm import ErrorManager

LOGGING_DIR = '/var/log/skarma'


def setup_logging_ui() -> None:
    """
    Setup logging into /var/log. If app don't have permission
    to access /var/log/skarma, than it will launch chmod to get
    it. Entering sudo password may be needed.
    """

    if not path.exists(LOGGING_DIR) or not path.isdir(LOGGING_DIR) or not os.access(LOGGING_DIR, os.W_OK):
        ErrorManager().report_error("Logging problem", "Can't access logging directory. Logging will be turned off.")
        print(f'Can\'t access logging directory.\n'
              f'Please, run "sudo mkdir -p {LOGGING_DIR} && sudo chown $(whoami) {LOGGING_DIR}"\n'
              f'Logging will be turned off.')
        return

    formatter = logging.Formatter('%(asctime)s - %(process)d - %(threadName)s (%(thread)d) '
                                  '- %(levelname)s - %(module)s - %(message)s')

    tglogger = logging.getLogger("telegram.bot")
    tglogger.setLevel(logging.DEBUG)

    tglogger.handlers = []

    botlogger = logging.getLogger('botlog')
    botlogger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    ifh = logging.handlers.TimedRotatingFileHandler(
        filename=path.join(LOGGING_DIR, 'bot-info.log'),
        when='d',
        backupCount=3
    )
    ifh.setLevel(logging.INFO)
    ifh.setFormatter(formatter)

    wfh = logging.handlers.TimedRotatingFileHandler(
        filename=path.join(LOGGING_DIR, 'bot-warn-error.log'),
        when='d',
        backupCount=7
    )
    wfh.setLevel(logging.WARN)
    wfh.setFormatter(formatter)

    tglogger.addHandler(sh)
    tglogger.addHandler(ifh)
    tglogger.addHandler(wfh)

    shm = logging.StreamHandler()
    shm.setLevel(logging.DEBUG)
    shm.setFormatter(formatter)

    ifhm = logging.handlers.TimedRotatingFileHandler(
        filename=path.join(LOGGING_DIR, 'debug.log'),
        when='d',
        backupCount=3
    )
    ifhm.setLevel(logging.DEBUG)
    ifhm.setFormatter(formatter)

    wfhm = logging.handlers.TimedRotatingFileHandler(
        filename=path.join(LOGGING_DIR, 'warn-error.log'),
        when='d',
        backupCount=7
    )
    wfhm.setLevel(logging.WARN)
    wfhm.setFormatter(formatter)

    botlogger.addHandler(shm)
    botlogger.addHandler(ifhm)
    botlogger.addHandler(wfhm)


if __name__ == "__main__":
    if sys.version_info < (3, 7):
        print('Invalid python version. Use python 3.7 or newer')

    if os.name != 'posix':
        print('Invalid os! Use any UNIX or Linux machine, including macOS')

    setup_logging_ui()

    blog = logging.getLogger('botlog')
    blog.info('Finished logging setup')
    blog.info('Starting bot')

    bot_info = AppInfo()

    blog.debug('Parsing arguments')
    parser = argparse.ArgumentParser(description=bot_info.app_description)

    parser.add_argument('--debug', '-d', help='Run bot dev version', action='store_true')

    result = parser.parse_args()
    DEBUG_MODE = result.debug

    if DEBUG_MODE:
        blog.info('Running in DEBUG mode')
        token = bot_info.app_dev_token
    else:
        blog.info('Running in INFO mode')
        token = bot_info.app_token

    blog.debug('Running with token: ' + token)

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    blog.info('Created updater and dispatcher')

    version_handler = CommandHandler('version', commands.version)
    dispatcher.add_handler(version_handler)
    blog.info('Added handler for /version command')

    if DEBUG_MODE:
        status_handler = CommandHandler('status', commands.status)
        dispatcher.add_handler(status_handler)
        blog.info('Added handler for /status command')

    report_handler = CommandHandler('bug_report', commands.bug_report)
    dispatcher.add_handler(report_handler)
    blog.info('Added handler for /bug_report command')

    support_handler = CommandHandler('support', commands.support)
    dispatcher.add_handler(support_handler)
    blog.info('Added handler for /support command')

    karma_handler = CommandHandler('my_karma', commands.my_karma)
    dispatcher.add_handler(karma_handler)
    blog.info('Added handler for /my_karma command')

    start_handler = CommandHandler('start', commands.start)
    dispatcher.add_handler(start_handler)
    blog.info('Added handler for /start command')

    top_handler = CommandHandler('top', commands.top)
    dispatcher.add_handler(top_handler)
    blog.info('Added handler for /top command')

    antitop_handler = CommandHandler('antitop', commands.antitop)
    dispatcher.add_handler(antitop_handler)
    blog.info('Added handler for /antitop command')

    if DEBUG_MODE:
        gen_error_handler = CommandHandler('gen_error', commands.gen_error)
        dispatcher.add_handler(gen_error_handler)
        blog.info('Added handler for /gen_error command')

    level_handler = CommandHandler('level', commands.level)
    dispatcher.add_handler(level_handler)
    blog.info('Added handler for /level command')

    message_handler = MessageHandler(Filters.reply & Filters.group & Filters.text & (~Filters.command), message_parser.message_handler)
    dispatcher.add_handler(message_handler)
    blog.info('Added handler for group reply messages')

    migrate_handler = MessageHandler(Filters.all, message_parser.handle_group_migration)
    dispatcher.add_handler(migrate_handler)
    blog.info('Added handler for group migration to supergroup')

    group_join_handler = MessageHandler(Filters.status_update.new_chat_members, message_parser.group_join_handler)
    dispatcher.add_handler(group_join_handler)
    blog.info('Added handler for group join')

    blog.info('Starting announcements thread')
    ann_thread = message_parser.AnnouncementsThread(updater.bot)
    ann_thread.start()

    blog.info('Starting polling')
    updater.start_polling()
