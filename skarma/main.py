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

from skarma import commands
from skarma.app_info import AppInfo

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    bot_info = AppInfo()

    updater = Updater(token=bot_info.app_dev_token, use_context=True)
    dispatcher = updater.dispatcher

    version_handler = CommandHandler('version', commands.version)
    dispatcher.add_handler(version_handler)

    updater.start_polling()
