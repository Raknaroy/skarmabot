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

from os import path

"""
Parse information from app.conf
"""
class AppInfo:

    APP_CONFIG_FILE = path.join(path.dirname(path.abspath(__file__)), '../config/app.conf')

    app_name: str
    app_description: str

    def __init__(self):
        if not path.isfile(config_file_path):
            print("Couldn't find config file path:", config_file_path, file=stderr)
            exit(2)
