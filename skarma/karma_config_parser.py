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

import datetime

from math import inf
from dataclasses import dataclass


@dataclass
class KarmaRange:
    """Karma range structure"""

    min_range: float
    max_range: float

    enable_plus: bool
    enable_minus: bool

    plus_value: int
    minus_value: int

    day_max: float
    timeout = datetime.timedelta

    def karma_in_range(self, karma: float) -> bool:
        """Check if user with given karma fits that karma range"""

        return (karma >= self.min_range) and (karma <= self.max_range)


class KarmaRangesManager:
    """Checks user's karma range. Karma ranges are loaded from karma.conf"""
    pass