#!/usr/bin/python
# -*- coding: utf-8 -*-

# find.py file is part of slpkg.

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


import os
from slpkg.blacklist import BlackList
from slpkg.splitting import split_package


def find_package(find_pkg, directory):
    """Find packages
    """
    pkgs = []
    if os.path.isdir(directory):
        installed = sorted(os.listdir(directory))
        blacklist = BlackList().packages(pkgs=installed, repo="local")
        if os.path.exists(directory):
            for pkg in installed:
                if (not pkg.startswith(".") and pkg.startswith(find_pkg) and
                        split_package(pkg)[0] not in blacklist):
                    pkgs.append(pkg)
    return pkgs
