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

import traceback
import pprint

from typing import List, Tuple, Type

from mysql.connector.errors import DatabaseError

from skarma.utils.singleton import SingletonMeta
from skarma.utils.db import DBUtils
from skarma.utils import email
from skarma.email_info import EmailInfo


class ErrorManager(metaclass=SingletonMeta):
    """
    Manage errors and exceptions.

    Errors are stored in 'errors' table in DB.
    """

    _dbu: DBUtils = DBUtils()

    report_by_email = True

    def get_all_errors(self) -> List[Tuple[int, str, str]]:
        """Get list of all reported errors from DB"""

        return self._dbu.run_single_query('select * from errors')

    def report_error(self, name: str, stacktrace: str) -> None:
        """Report new error to DB"""
        self._dbu.run_single_update_query('insert into skarma.errors (name, stacktrace) VALUES (%s, %s)', (name, stacktrace))

        if self.report_by_email:
            try:
                self._report_via_email(name, stacktrace)
            except Exception as e:
                pass  # TODO: Logging

    def report_exception(self, e: Exception) -> None:
        """Report new error to DB"""
        self.report_error(repr(e), ' '.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))

    def get_number_of_errors(self) -> int:
        """Returns number of reported errors in DB"""
        res_ = self._dbu.run_single_query("select count(*) from errors")

        if len(res_) != 1 or (len(res_[0]) != 1) or type(res_[0][0]) is not int:
            raise DatabaseError('Invalid response from DB (getting number of errors): ' + pprint.pformat(res_))

        return res_[0][0]

    @staticmethod
    def _report_via_email(name: str, stacktrace: str) -> None:
        """Send error report to email. See email.conf for more information"""
        email.send_email(EmailInfo().user_to, 'Error in SKarma: ' + name, stacktrace)  # TODO: Replce name
