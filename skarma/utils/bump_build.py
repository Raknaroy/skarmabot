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
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SKarma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SKarma. If not, see <https://www.gnu.org/licenses/>.

from __future__ import print_function

from os import path
from sys import stderr
from configparser import ConfigParser

if __name__ == "__main__":
    config_file_path = path.join(path.dirname(path.abspath(__file__)), '../../config/app.conf')

    if not path.isfile(config_file_path):
        print("Couldn't find config file path:", config_file_path, file=stderr)
        exit(2)

    app_config = ConfigParser()
    app_config.read(config_file_path)

    build = int(app_config['GENERAL']['bot_build'], 16)
    build += 1
    app_config['GENERAL']['bot_build'] = "{0:0{1}x}".format(build, 5)

    with open(config_file_path, 'w') as f:
        app_config.write(f)
