#!/usr/bin/python
# -*- coding: utf-8 -*-

# slack_version.py file is part of slpkg.

# Copyright 2014-2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
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


import re

from slpkg.utils import Utils


def slack_ver():
    """
    Open file and read Slackware version
    """
    sv = Utils().read_file("/etc/slackware-version")
    version = re.findall(r"\d+", sv)
    if len(sv) > 2:
        return (".".join(version[:2]))
    else:
        return (".".join(version))
