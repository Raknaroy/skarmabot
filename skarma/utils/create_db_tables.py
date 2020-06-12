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

"""
This file contains functions that create empty DB
tables for project. Run this file to create it
automatically.
"""

from typing import List, Callable

from mysql.connector.errors import DatabaseError

from skarma.utils.db import DBUtils


def create_error_table(dbu: DBUtils):
    tables = dbu.run_single_query("SHOW TABLES;")
    if tuple('errors') in tables:
        raise DatabaseError("Table 'errors' already exists")

    dbu.run_single_update_query("""create table errors
                               (
                                 id int auto_increment,
                                 name text not null,
                                 stacktrace longtext null,
                                 constraint errors_pk
                                  primary key (id)
                               );""")


def _run_functions_and_print_db_errors(functions: List[Callable[[DBUtils], None]], dbu: DBUtils):
    for fun in functions:
        try:
            fun(dbu)
        except DatabaseError as e:
            print(e.msg)


if __name__ == '__main__':
    dbu = DBUtils()

    _run_functions_and_print_db_errors([create_error_table], dbu)
    print('Done.')
