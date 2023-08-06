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

"""Tests for :mod:`gwosc.utils`
"""

import pytest

from .. import utils

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


def test_url_segment():
    seg = utils.url_segment('X-TEST-123-456.ext')
    assert seg == (123, 579)


@pytest.mark.parametrize('url, segment, result', [
    ('A-B-10-1.ext', (0, 10), False),
    ('A-B-10-1.ext', (5, 11), True),
    ('A-B-10-1.ext', (10, 15), True),
    ('A-B-10-1.ext', (11, 15), False),
])
def test_url_overlaps_segment(url, segment, result):
    assert utils.url_overlaps_segment(url, segment) is result


@pytest.mark.remote
@pytest.mark.parametrize('segment, result', [
    ((0, 64), True),
    ((1, 63), True),
    ((-1, 63), False),
    ((-1, 64), False),
    ((0, 65), False),
    ((1, 65), False),
    ((-1, 64), False),
])
def test_full_coverage(mock_urls, segment, result):
    assert utils.full_coverage(mock_urls, segment) is result


def test_full_coverage_empty():
    assert utils.full_coverage([], (0, 1)) is False


@pytest.mark.parametrize('seg1, seg2, result', [
    ((10, 11), (0, 10), False),
    ((10, 11), (5, 11), True),
    ((10, 11), (10, 15), True),
    ((10, 11), (11, 15), False),
])
def test_segments_overlap(seg1, seg2, result):
    assert utils.segments_overlap(seg1, seg2) is result
