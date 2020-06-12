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

from os import path
from configparser import ConfigParser


class AppInfo:
    """Parse information from app.conf"""

    APP_CONFIG_FILE = path.join(path.dirname(path.abspath(__file__)), '../config/app.conf')

    app_name: str
    app_description: str
    app_version: str
    app_build: str

    app_token: str
    app_dev_token: str

    def __init__(self):
        """
        Parse config file and fill all fields.

        Raise FileNotFoundError if file doesn't exist
        """

        if not path.isfile(self.APP_CONFIG_FILE):
            raise FileNotFoundError("Couldn't find config file path: " + self.APP_CONFIG_FILE)

        app_config = ConfigParser()
        app_config.read(self.APP_CONFIG_FILE)

        self.app_name = app_config['GENERAL']['bot_name']
        self.app_description = app_config['GENERAL']['bot_desc']
        self.app_version = app_config['GENERAL']['bot_version']
        self.app_build = app_config['GENERAL']['bot_build']

        self.app_token = app_config['TOKENS']['token']
        self.app_dev_token = app_config['TOKENS']['dev_token']
