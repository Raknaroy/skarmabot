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


def create_karma_table(dbu: DBUtils):
    tables = dbu.run_single_query("SHOW TABLES;")
    if tuple('karma') in tables:
        raise DatabaseError("Table 'karma' already exists")

    dbu.run_single_update_query("""create table karma
                                   (
                                        id int auto_increment,
                                        chat_id text not null,
                                        user_id text not null,
                                        karma int default 0 not null,
                                        constraint karma_pk
                                            primary key (id)
                                   );""")


def create_chats_table(dbu: DBUtils):
    tables = dbu.run_single_query("SHOW TABLES;")
    if tuple('chats') in tables:
        raise DatabaseError("Table 'chats' already exists")

    dbu.run_single_update_query("""create table chats
                                   (
                                        id int auto_increment,
                                        chat_id text not null,
                                        constraint chats_pk
                                            primary key (id)
                                   );

""")


def create_announcements_table(dbu: DBUtils):
    tables = dbu.run_single_query("SHOW TABLES;")
    if tuple('announcements') in tables:
        raise DatabaseError("Table 'announcements' already exists")

    dbu.run_single_update_query("""create table announcements
                                   (
                                     id int auto_increment,
                                     text longtext not null,
                                     constraint announcements_pk
                                      primary key (id)
                                   );""")


def create_usernames_table(dbu: DBUtils):
    tables = dbu.run_single_query("SHOW TABLES;")
    if tuple('usernames') in tables:
        raise DatabaseError("Table 'usernames' already exists")

    dbu.run_single_update_query("""create table usernames
                                   (
                                     id int auto_increment,
                                     user_id text not null,
                                     name text not null,
                                     constraint usernames_pk
                                      primary key (id)
                                   );""")

    dbu.run_single_update_query("create unique index usernames_user_id_uindex on usernames (user_id(255));")


def create_stats_table(dbu: DBUtils):
    tables = dbu.run_single_query("SHOW TABLES;")
    if tuple('stats') in tables:
        raise DatabaseError("Table 'stats' already exists")

    dbu.run_single_update_query("""create table stats
                                   (
                                     id int auto_increment,
                                     chat_id text not null,
                                     user_id text not null,
                                     last_karma_change datetime not null,
                                     today date not null,
                                     today_karma_changes int not null,
                                     constraint stats_pk
                                      primary key (id)
                                   );""")

    dbu.run_single_update_query('alter table stats add unique unique_index(chat_id(255), user_id(255));')


def create_messages_table(dbu: DBUtils):
    tables = dbu.run_single_query("SHOW TABLES;")
    if tuple('messages') in tables:
        raise DatabaseError("Table 'messages' already exists")

    dbu.run_single_update_query("""create table messages
                                   (
                                     id int auto_increment,
                                     message_id text null,
                                     chat_id text not null,
                                     user_id text not null,
                                     constraint messages_pk
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

    _run_functions_and_print_db_errors([create_error_table, create_karma_table,
                                        create_chats_table, create_announcements_table,
                                        create_usernames_table, create_stats_table,
                                        create_messages_table], dbu)
    print('Done.')
