#!/usr/bin/python
# -*- coding: utf-8 -*-

# remove.py file is part of slpkg.

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

import os

<<<<<<< HEAD:slpkg/remove.py
from __metadata__ import MetaData as _m
=======
from __metadata__ import del_all
>>>>>>> master:slpkg/remove.py


def delete(path, packages):
    '''
    Remove downloaded packages
    '''
<<<<<<< HEAD:slpkg/remove.py
    if _m.del_all == "on":
=======
    if del_all == "on":
>>>>>>> master:slpkg/remove.py
        for pkg in packages:
            os.remove(path + pkg)
