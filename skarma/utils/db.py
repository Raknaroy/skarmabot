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

import mysql.connector

from mysql.connector import MySQLConnection
from typing import List, Tuple, Any, Union

from skarma.db_info import DBInfo
from skarma.utils.singleton import SingletonMeta


class DBUtils(metaclass=SingletonMeta):

    _botdb: Union[MySQLConnection, None] = None

    def __init__(self) -> None:
        """
        Init global botdb variable with new MySql connection.
        """
        dbi = DBInfo()

        self._botdb = mysql.connector.connect(
            host=dbi.host,
            port=dbi.port,
            user=dbi.user,
            password=dbi.password,
            database=dbi.database
        )

        self.run_single_update_query('SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED')

    def run_single_query(self, operation: str, params=()) -> List[Tuple[Any]]:
        """
        Run SELECT query to db that don't update DB. Use run_single_update_query
        if your query updated DB.
        Arguments will be passed to MySQLCursor.execute().

        ProgrammingError will be raised on error.

        Consider using 'params' argument instead of others string building methods
        to avoid SQL injections. You can report SQL injections problems found in
        the project at https://github.com/sandsbit/skarmabot/security/advisories/new.
        """
        cursor_ = self._botdb.cursor()
        cursor_.execute(operation, params)

        res_ = cursor_.fetchall()
        cursor_.close()
        return res_

    def run_single_update_query(self, operation: str, params=()) -> None:
        """
        Run query to db that do update DB. Use run_single_query instead
        if you are doing SELECT query .
        Arguments will be passed to MySQLCursor.execute().

        ProgrammingError will be raised on error.

        Consider using 'params' argument instead of others string building methods
        to avoid SQL injections. You can report SQL injections problems found in
        the project at https://github.com/sandsbit/skarmabot/security/advisories/new.
        """
        cursor_ = self._botdb.cursor()
        cursor_.execute(operation, params)

        self._botdb.commit()
        cursor_.close()

    def is_connected(self) -> bool:
        return self._botdb.is_connected()

