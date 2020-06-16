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
import logging

from math import inf
from configparser import ConfigParser, SectionProxy
from os import path
from typing import List, Optional
from dataclasses import dataclass


class ConfigParseError(Exception):
    pass


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

    @staticmethod
    def _read_int_or_inf(from_: str) -> float:
        if from_ == 'oo' or from_ == '+oo':
            return inf
        elif from_ == '-oo':
            return -inf
        else:
            return int(from_)

    @classmethod
    def range_from_parsed_config(cls, parsed: SectionProxy):
        """Create KarmaRange from parsed section"""
        blog = logging.getLogger('botlog')
        blog.info(f'Parsing section {parsed.name}')

        try:
            cls.min_range = cls._read_int_or_inf(parsed['min_range']),
            cls.max_range = cls._read_int_or_inf(parsed['max_range']),
            cls.enable_plus = parsed.getboolean('enable_plus'),
            cls.enable_minus = parsed.getboolean('enable_minus'),
            cls.plus_value = parsed.getint('plus_value'),
            cls.minus_value = parsed.getint('minus_value'),
            cls.day_max = cls._read_int_or_inf(parsed['day_max']),

            timeout_v = int(parsed['timeout'][:-1])
            timeout_s = parsed['timeout'][-1]

            if timeout_s == 's':
                cls.timeout = datetime.timedelta(seconds=timeout_v)
            elif timeout_s == 'm':
                cls.timeout = datetime.timedelta(minutes=timeout_v)
            elif timeout_s == 'h':
                cls.timeout = datetime.timedelta(hours=timeout_v)
            elif timeout_s == 'd':
                cls.timeout = datetime.timedelta(days=timeout_v)
            elif timeout_s == 'w':
                cls.timeout = datetime.timedelta(weeks=timeout_v)
        except KeyError as e:
            msg = f'Value of {str(e)} not found for section {parsed.name}'
            blog.fatal(msg)
            raise ConfigParseError(msg)


class KarmaRangesManager:
    """Checks user's karma range. Karma ranges are loaded from karma.conf"""
    pass