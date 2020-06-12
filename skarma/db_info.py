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
    """Parse information from db.conf"""

    DB_CONFIG_FILE = path.join(path.dirname(path.abspath(__file__)), '../config/db.conf')

    host: str
    port: int

    user: str
    password: str
    database: str

    def __init__(self):
        """
        Parse config file and fill all fields.

        Raise FileNotFoundError if file doesn't exist
        """

        if not path.isfile(self.DB_CONFIG_FILE):
            raise FileNotFoundError("Couldn't find DB config file path: " + self.DB_CONFIG_FILE)

        app_config = ConfigParser()
        app_config.read(self.DB_CONFIG_FILE)

        self.host = app_config['GENERAL']['host']
        self.port = int(app_config['GENERAL']['port'])

        self.user = app_config['LOGIN']['user']
        self.password = app_config['LOGIN']['password']
        self.database = app_config['LOGIN']['database']
