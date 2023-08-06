# -*- coding: utf-8 -*-
# Copyright (C) Cardiff University, 2018-2020
#
# This file is part of GWOSC.
#
# GWOSC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWOSC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWOSC.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for :mod:`gwosc.timeline`
"""

from unittest import mock

import pytest

from .. import timeline

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


@pytest.mark.remote
@pytest.mark.parametrize('flag, start, end, result', [
    ('H1_DATA', 1126051217, 1126151217, [
        (1126073529, 1126114861),
        (1126121462, 1126123267),
        (1126123553, 1126126832),
        (1126139205, 1126139266),
        (1126149058, 1126151217),
    ]),
    ('L1_DATA', 1126259446, 1126259478, [
        (1126259446, 1126259478),
    ])
])
def test_get_segments(flag, start, end, result):
    assert timeline.get_segments(flag, start, end) == result


@pytest.mark.remote
def test_get_segments_long():
    assert len(timeline.get_segments('H1_DATA', 1126051217, 1137196817)) == 654


@pytest.mark.remote
def test_timeline_url():
    # check that unknown IFO results in no matches
    with pytest.raises(ValueError):
        timeline.timeline_url('X1', 1126259446, 1126259478)


@mock.patch('gwosc.timeline._find_dataset', return_value='S6')
def test_timeline_url_local(find):
    assert timeline.timeline_url('L1_DATA', 0, 1, host='test') == (
        'test/timeline/segments/json/S6/L1_DATA/0/1/')
    find.assert_called_with(0, 1, 'L1', host='test')
