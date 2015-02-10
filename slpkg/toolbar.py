#!/usr/bin/python
# -*- coding: utf-8 -*-

# toolbar.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import time

<<<<<<< HEAD:slpkg/toolbar.py
from __metadata__ import MetaData as _m
=======
from __metadata__ import color
>>>>>>> master:slpkg/toolbar.py


def status(index, width, step):
    '''
    Print toolbar status
    '''
    if index == width:
<<<<<<< HEAD:slpkg/toolbar.py
        sys.stdout.write("{0}.{1}".format(_m.color['GREY'], _m.color['ENDC']))
        sys.stdout.flush()
        width += step
        time.sleep(0.02)
=======
        sys.stdout.write("{0}.{1}".format(color['GREY'], color['ENDC']))
        sys.stdout.flush()
        width += step
        time.sleep(0.05)
>>>>>>> master:slpkg/toolbar.py
    return width
