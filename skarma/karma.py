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

from skarma.utils.singleton import SingletonMeta
from skarma.utils.db import DBUtils


class KarmaManager(metaclass=SingletonMeta):
    """Api to work with karma table in database"""

    blog = logging.getLogger('botlog')
    db = DBUtils()

    def get_user_karma(self, chat_id: int, user_id: int) -> int:
        pass

    def set_user_karma(self, chat_id: int, user_id: int) -> None:
        pass

    def clean_user_karma(self, chat_id: int, user_id: int) -> None:
        pass

    def clean_chat_karma(self, chat_id: int) -> None:
        pass

    def change_user_karma(self, chat_id: int, user_id: int, change: int) -> None:
        pass

    def increase_user_karma(self, chat_id: int, user_id: int, up_change: int) -> None:
        pass

    def decrease_user_karma(self, chat_id: int, user_id: int, down_change: int) -> None:
        pass