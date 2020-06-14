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

from telegram.ext import Updater, CommandHandler
import logging
import logging.handlers
import os

from os import path

from skarma import commands
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
        print(f'Can\t access logging directory.\n'
              f'Please, run "sudo mkdir -p {LOGGING_DIR} && sudo chown $(whoami) {LOGGING_DIR}"\n'
              f'Logging will be turned off.')
        return

    formatter = logging.Formatter('%(asctime)s - %(process)d - %(levelname)s - %(module)s - %(message)s')

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
    setup_logging_ui()

    blog = logging.getLogger('botlog')
    blog.info('Finished logging setup')
    blog.info('Starting bot')

    bot_info = AppInfo()

    updater = Updater(token=bot_info.app_dev_token, use_context=True)
    dispatcher = updater.dispatcher

    version_handler = CommandHandler('version', commands.version)
    dispatcher.add_handler(version_handler)

    version_handler = CommandHandler('status', commands.status)
    dispatcher.add_handler(version_handler)

    updater.start_polling()
