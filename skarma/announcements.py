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

from typing import List, Tuple

from mysql.connector.errors import DatabaseError

from skarma.utils.singleton import SingletonMeta
from skarma.utils.db import DBUtils


class ChatsManager(metaclass=SingletonMeta):
    """Store list of all bot's chats in database"""

    blog = logging.getLogger('botlog')
    db: DBUtils = DBUtils()

    def get_all_chats(self) -> List[int]:
        """Returns list of IDs of all bot's chats"""
        resp = self.db.run_single_query('select * from chats')
        result = [i[1] for i in resp]
        return result

    def add_new_chat(self, id_: int) -> None:
        """Add new bot's chat id"""
        result = self.db.run_single_query('select * from chats where chat_id = %s', [id_])
        if len(result) == 0:
            self.db.run_single_update_query('insert into skarma.chats (chat_id) VALUES (%s)', [id_])


class AnnouncementsManager(metaclass=SingletonMeta):
    """Add or get announcements from database"""

    blog = logging.getLogger('botlog')
    db: DBUtils = DBUtils()

    def get_all_announcements(self) -> List[Tuple[int, str]]:
        """Returs list of tuples, that store announcements' IDs and messages"""

        return self.db.run_single_query('select * from announcements')

    def add_new_announcement(self, msg: str) -> None:
        """Add new annoucement to database"""

        self.db.run_single_update_query('insert into skarma.announcements (text) VALUES (%s)', [msg])

    def delete_announcement(self, id_: int) -> None:
        """Delete announcement from database by its id"""

        self.db.run_single_query('delete from announcements where id = %s', [id_])
