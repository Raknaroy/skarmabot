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

from typing import List, Tuple

from skarma.utils.singleton import SingletonMeta


class ErrorManager(metaclass=SingletonMeta):
    """
    Manage errors and exceptions.

    Errors are stored in 'errors' table in DB.
    """

    def get_all_errors(self) -> List[Tuple[int, str, str]]:
        """Get list of all reported errors from DB"""
        pass

    def report_error(self, name: str, stacktrace: str) -> None:
        """Report new error to DB"""
        pass

    def report_exception(self, e: Exception) -> None:
        """Report new error to DB"""
        pass

    def get_number_of_errors(self) -> int:
        """Returns number of reported errors in DB"""
        pass

    def _report_via_email(self, name: str, stacktrace: str) -> None:
        """Send error report to email. See email.conf for more information"""
        pass
