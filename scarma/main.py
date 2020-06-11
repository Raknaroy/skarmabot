#  ____   ____
# / ___| / ___|__ _ _ __ _ __ ___   __ _
# \___ \| |   / _` | '__| '_ ` _ \ / _` |
#  ___) | |__| (_| | |  | | | | | | (_| |
# |____/ \____\__,_|_|  |_| |_| |_|\__,_|
#
# Yet another carma bot for telegram
# Copyright (C) 2020 Nikita Serba. All rights reserved
#
# SCarma is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SCarma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SCarma. If not, see <https://www.gnu.org/licenses/>.

from telegram.ext import Updater, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    updater = Updater(token='<token>', use_context=True)
    dispatcher = updater.dispatcher

    updater.start_polling()
