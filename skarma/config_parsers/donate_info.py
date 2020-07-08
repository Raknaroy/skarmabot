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

from os import path
from configparser import ConfigParser

from skarma.utils.singleton import SingletonMeta


class DonateInfo(metaclass=SingletonMeta):
    """Parse information from donate.conf"""

    blog = logging.getLogger('botlog')

    DONATE_CONFIG_FILE = path.join(path.dirname(path.abspath(__file__)), '../../config/donate.conf')

    test_enabled: bool
    test_payload: str
    test_provider_token: str
    test_start_parameter: str

    enabled: bool
    payload: str
    provider_token: str
    start_parameter: str

    def __init__(self):
        """
        Parse config file and fill all fields.

        Raise FileNotFoundError if file doesn't exist
        """

        self.blog.info('Creating new DonateInfo class instance')
        self.blog.debug('Reading debug info file from : ' + path.abspath(self.DONATE_CONFIG_FILE))

        if not path.isfile(self.DONATE_CONFIG_FILE):
            msg = "Couldn't find debug config file path: " + self.DONATE_CONFIG_FILE
            self.blog.error(msg)
            raise FileNotFoundError(msg)

        app_config = ConfigParser()
        app_config.read(self.DONATE_CONFIG_FILE)

        self.blog.debug('Successfully debug config file')

        self.test_enabled = app_config['TEST'].getboolean('enabled')
        self.test_payload = app_config['TEST']['payload']
        self.test_provider_token = app_config['TEST']['provider_token']
        self.test_start_parameter = app_config['TEST']['start_parameter']

        self.enabled = app_config['RELEASE'].getboolean('enabled')
        self.payload = app_config['RELEASE']['payload']
        self.provider_token = app_config['RELEASE']['provider_token']
        self.start_parameter = app_config['RELEASE']['start_parameter']
