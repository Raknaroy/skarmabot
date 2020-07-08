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

from typing import List


class NotFound(Exception):
    pass


def binary_search(obj, lst: List) -> int:
    """
    Find obj in lst using binary search. lst should be sorted.

    All members of lst should support == (__eq__) operators with the type of obj. Also,
    '<' must be supported between obj and lst elements.

    Raises NotFound if obj is not in lst.
    If lst is not sorted or obj occur in lst several time, function
    behavior is undefined.
    """
    lst_len = len(lst)
    if lst_len == 0:
        raise NotFound

    pos = int(lst_len / 2)
    if lst[pos] == obj:
        return pos
    elif obj < lst[pos]:
        return binary_search(obj, lst[0:pos])
    else:
        return pos + 1 + binary_search(obj, lst[pos+1:])
