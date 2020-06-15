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
from pprint import pformat

from mysql.connector.errors import DatabaseError

from skarma.utils.singleton import SingletonMeta
from skarma.utils.db import DBUtils


class NoSuchUser(Exception):
    pass


class UsernamesManager:
    """Associate user's id with username"""

    blog = logging.getLogger('botlog')
    db: DBUtils = DBUtils()

    def get_username_by_id(self, id_: int) -> str:
        """Get user's name from database by his id. NoSuchUser will be thrown if there is no such user id in database"""
        self.blog.info(f'Getting username of user with id #{id_}')

        result = self.db.run_single_query('select name from usernames where user_id = %s', [id_])

        if len(result) == 0:
            raise NoSuchUser
        elif len(result) != 1:
            msg = f"Too many names associated with user with id #{id_}"
            self.blog.error(msg)
            raise DatabaseError(msg)
        else:
            return result[0][0]

    def set_username(self, id_: int, name: str) -> None:
        """Set name of user with given id"""
        self.blog.info(f'Setting username of user with id #{id_} to "{name}"')

        self.db.run_single_update_query('insert into usernames (user_id, name) values (%(id)s, %(name)s) '
                                        'on duplicate key update name = %(name)s', {'id': id_, 'name': name})


class KarmaManager(metaclass=SingletonMeta):
    """Api to work with karma table in database"""

    blog = logging.getLogger('botlog')
    db: DBUtils = DBUtils()

    def get_user_karma(self, chat_id: int, user_id: int) -> int:
        self.blog.debug(f'Getting karma of user #{user_id} in chat #{chat_id}')
        result = self.db.run_single_query('select karma from karma where chat_id = %s and user_id = %s',
                                          (chat_id, user_id))
        if len(result) == 0:
            return 0

        if (len(result) != 1) or (len(result[0]) != 1):
            msg = 'Invalid database response for getting user karma: ' + pformat(result)
            self.blog.error('Invalid database response for getting user karma: ' + pformat(result))
            raise DatabaseError(msg)

        return result[0][0]

    def set_user_karma(self, chat_id: int, user_id: int) -> None:  # TODO
        pass

    def clean_user_karma(self, chat_id: int, user_id: int) -> None:
        pass

    def clean_chat_karma(self, chat_id: int) -> None:
        pass

    def change_user_karma(self, chat_id: int, user_id: int, change: int) -> None:
        result = self.db.run_single_query('select * from karma where chat_id = %s and user_id = %s', (chat_id, user_id))
        if len(result) == 0:
            self.db.run_single_update_query('insert into skarma.karma (chat_id, user_id, karma) VALUES (%s, %s, %s)',
                                            (chat_id, user_id, change))
        else:
            self.db.run_single_update_query('update karma set karma = karma + %s where chat_id = %s and user_id = %s',
                                        (change, chat_id, user_id))

    def increase_user_karma(self, chat_id: int, user_id: int, up_change: int) -> None:
        self.change_user_karma(chat_id, user_id, up_change)

    def decrease_user_karma(self, chat_id: int, user_id: int, down_change: int) -> None:
        self.change_user_karma(chat_id, user_id, -down_change)

    def get_ordered_karma_top(self, chat_id: int, amount: int = 5, biggest: bool = True) -> List[Tuple[int, int]]:
        """
        Get ordered *amount* people from chat with biggedt (biggest = True) or smallest (biggest = False) karma.
        Returns list with tuples, which contain users' IDs and karma
        """

        order = 'desc' if biggest else 'asc'
        symbol = '>'if biggest else '<'
        return self.db.run_single_query(f'select distinct user_id, karma from karma where chat_id = %s and karma {symbol} 0 '
                                 f'order by karma {order} limit %s',
                                 [chat_id, amount])
