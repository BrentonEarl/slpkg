#!/usr/bin/python
# -*- coding: utf-8 -*-

# tracking.py file is part of slpkg.

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

<<<<<<< HEAD

from utils import Utils
from messages import Msg
from __metadata__ import MetaData as _m
=======
import sys

from messages import (
    template
)
from __metadata__ import (
    pkg_path,
    color,
    sp
)
>>>>>>> master

from pkg.find import find_package

from sbo.search import sbo_search_pkg
<<<<<<< HEAD
from sbo.dependency import Requires

from binary.search import search_pkg
from binary.dependency import Dependencies
=======
from sbo.dependency import sbo_dependencies_pkg

from others.search import search_pkg
from others.dependency import dependencies_pkg
>>>>>>> master


def track_dep(name, repo):
    '''
    View tree of dependencies and also
    highlight packages with color green
    if allready installed and color red
    if not installed.
    '''
<<<<<<< HEAD
    Msg().resolving()
    if repo == "sbo":
        dependencies_list = Requires().sbo(name)
        find_pkg = sbo_search_pkg(name)
    else:
        PACKAGES_TXT = Utils().read_file(_m.lib_path + '{0}_repo/'
                                         'PACKAGES.TXT'.format(repo))
        dependencies_list = Dependencies(PACKAGES_TXT, repo).binary(name)
        find_pkg = search_pkg(name, repo)
    Msg().done()
    if find_pkg:
        requires, dependencies = [], []
        requires = Utils().dimensional_list(dependencies_list)
        requires.reverse()
        dependencies = Utils().remove_dbs(requires)
=======
    sys.stdout.write("{0}Reading package lists ...{1}".format(color['GREY'],
                                                              color['ENDC']))
    sys.stdout.flush()
    if repo == "sbo":
        dependencies_list = sbo_dependencies_pkg(name)
        find_pkg = sbo_search_pkg(name)
    else:
        dependencies_list = dependencies_pkg(name, repo)
        find_pkg = search_pkg(name, repo)
    sys.stdout.write("{0}Done{1}\n".format(color['GREY'], color['ENDC']))
    if find_pkg:
        requires, dependencies = [], []
        # Create one list for all packages
        for pkg in dependencies_list:
            requires += pkg
        requires.reverse()
        # Remove double dependencies
        for duplicate in requires:
            if duplicate not in dependencies:
                dependencies.append(duplicate)
>>>>>>> master
        if dependencies == []:
            dependencies = ["No dependencies"]
        pkg_len = len(name) + 24
        print("")    # new line at start
<<<<<<< HEAD
        Msg().template(pkg_len)
        print("| Package {0}{1}{2} dependencies :".format(_m.color['CYAN'],
                                                          name,
                                                          _m.color['ENDC']))
        Msg().template(pkg_len)
        print("\\")
        print(" +---{0}[ Tree of dependencies ]{1}".format(_m.color['YELLOW'],
                                                           _m.color['ENDC']))
        index = 0
        for pkg in dependencies:
            index += 1
            if find_package(pkg + _m.sp, _m.pkg_path):
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index,
                                                  _m.color['GREEN'],
                                                  pkg, _m.color['ENDC']))
            else:
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, _m.color['RED'],
                                                  pkg, _m.color['ENDC']))
=======
        template(pkg_len)
        print("| Package {0}{1}{2} dependencies :".format(color['CYAN'], name,
                                                          color['ENDC']))
        template(pkg_len)
        print("\\")
        print(" +---{0}[ Tree of dependencies ]{1}".format(color['YELLOW'],
                                                           color['ENDC']))
        index = 0
        for pkg in dependencies:
            index += 1
            if find_package(pkg + sp, pkg_path):
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, color['GREEN'],
                                                  pkg, color['ENDC']))
            else:
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, color['RED'],
                                                  pkg, color['ENDC']))
>>>>>>> master
        print("")    # new line at end
    else:
        print("\nNo package was found to match\n")
