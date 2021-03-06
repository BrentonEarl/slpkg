#!/usr/bin/python
# -*- coding: utf-8 -*-

# install.py file is part of slpkg.

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

from slpkg.utils import Utils
from slpkg.sizes import units
from slpkg.messages import Msg
from slpkg.toolbar import status
from slpkg.checksum import check_md5
from slpkg.blacklist import BlackList
from slpkg.downloader import Download
from slpkg.log_deps import write_deps
from slpkg.grep_md5 import pkg_checksum
from slpkg.remove import delete_package
from slpkg.splitting import split_package
from slpkg.__metadata__ import MetaData as _meta_

from slpkg.pkg.find import find_package
from slpkg.pkg.manager import PackageManager
from slpkg.pkg.installed import GetFromInstalled

from slpkg.binary.greps import repo_data
from slpkg.binary.repo_init import RepoInit
from slpkg.binary.dependency import Dependencies


class BinaryInstall(object):
    """Install binaries packages with all dependencies from
    repository
    """
    def __init__(self, packages, repo, flag):
        self.packages = packages
        self.repo = repo
        self.flag = flag
        self.meta = _meta_
        self.msg = Msg()
        self.version = self.meta.slack_rel
        self.tmp_path = self.meta.slpkg_tmp_packages
        for fl in self.flag:
            if fl.startswith("--directory-prefix="):
                self.tmp_path = fl.split("=")[1]
                if not self.tmp_path.endswith("/"):
                    self.tmp_path += "/"
        self.dwn, self.dep_dwn = [], []
        self.install, self.dep_install = [], []
        self.comp_sum, self.dep_comp_sum = [], []
        self.uncomp_sum, self.dep_uncomp_sum = [], []
        self.dependencies = []
        self.deps_dict = {}
        self.answer = ""
        self.msg.reading()
        self.PACKAGES_TXT, self.mirror = RepoInit(self.repo).fetch()
        self.data = repo_data(self.PACKAGES_TXT, self.repo, self.flag)
        self.blacklist = BlackList().packages(self.data[0], self.repo)

    def start(self, if_upgrade):
        """
        Install packages from official Slackware distribution
        """
        self.case_insensitive()
        # fix if packages is for upgrade
        self.if_upgrade = if_upgrade
        mas_sum = dep_sum = sums = [0, 0, 0]
        self.msg.done()
        self.dependencies = self.resolving_deps()
        self.update_deps()
        (self.dep_dwn, self.dep_install, self.dep_comp_sum,
            self.dep_uncomp_sum) = self.store(self.dependencies)
        self.clear_masters()
        (self.dwn, self.install, self.comp_sum,
            self.uncomp_sum) = self.store(self.packages)
        if (self.meta.rsl_deps in ["on", "ON"] and
                "--resolve-off" not in self.flag):
            self.msg.done()
        if self.install:
            print("\nThe following packages will be automatically "
                  "installed or upgraded \nwith new version:\n")
            self.top_view()
            self.msg.upg_inst(self.if_upgrade)
            mas_sum = self.views(self.install, self.comp_sum)
            if self.dependencies:
                print("Installing for dependencies:")
                dep_sum = self.views(self.dep_install, self.dep_comp_sum)
            # sums[0] --> installed
            # sums[1] --> upgraded
            # sums[2] --> uninstall
            sums = [sum(i) for i in zip(mas_sum, dep_sum)]
            unit, size = units(self.comp_sum + self.dep_comp_sum,
                               self.uncomp_sum + self.dep_uncomp_sum)
            print("\nInstalling summary")
            print("=" * 79)
            print("{0}Total {1} {2}.".format(self.meta.color["GREY"],
                                             sum(sums),
                                             self.msg.pkg(sum(sums))))
            print("{0} {1} will be installed, {2} will be upgraded and "
                  "{3} will be reinstalled.".format(sums[2],
                                                    self.msg.pkg(sums[2]),
                                                    sums[1], sums[0]))
            print("Need to get {0} {1} of archives.".format(size[0],
                                                            unit[0]))
            print("After this process, {0} {1} of additional disk "
                  "space will be used.{2}".format(size[1], unit[1],
                                                  self.meta.color["ENDC"]))
            print("")
            if self.msg.answer() in ["y", "Y"]:
                self.install.reverse()
                Download(self.tmp_path, self.dep_dwn + self.dwn,
                         self.repo).start()
                if "--download-only" in self.flag:
                    raise SystemExit()
                self.dep_install = Utils().check_downloaded(
                    self.tmp_path, self.dep_install)
                self.install = Utils().check_downloaded(
                    self.tmp_path, self.install)
                ins, upg = self.install_packages()
                self.msg.reference(ins, upg)
                write_deps(self.deps_dict)
                delete_package(self.tmp_path, self.install)
        else:
            self.msg.not_found(self.if_upgrade)

    def case_insensitive(self):
        """Matching packages distinguish between uppercase and
        lowercase
        """
        if "--case-ins" in self.flag:
            data = []
            data = Utils().package_name(self.PACKAGES_TXT)
            data_dict = Utils().case_sensitive(data)
            for pkg in self.packages:
                index = self.packages.index(pkg)
                for key, value in data_dict.iteritems():
                    if key == pkg.lower():
                        self.packages[index] = value

    def update_deps(self):
        """Update dependencies dictionary with all package
        """
        for dep in self.dependencies:
            deps = Utils().dimensional_list(Dependencies(
                self.PACKAGES_TXT, self.repo, self.blacklist).binary(
                    dep, self.flag))
            self.deps_dict[dep] = deps

    def clear_masters(self):
        """Clear master packages if already exist in dependencies
        or if added to install two or more times
        """
        packages = []
        for mas in Utils().remove_dbs(self.packages):
            if mas not in self.dependencies:
                packages.append(mas)
        self.packages = packages

    def install_packages(self):
        """Install or upgrade packages
        """
        installs, upgraded = [], []
        for inst in (self.dep_install + self.install):
            package = (self.tmp_path + inst).split()
            pkg_ver = "{0}-{1}".format(split_package(inst)[0],
                                       split_package(inst)[1])
            self.checksums(inst)
            if os.path.isfile(self.meta.pkg_path + inst[:-4]):
                print("[ {0}reinstalling{1} ] --> {2}".format(
                    self.meta.color["GREEN"], self.meta.color["ENDC"], inst))
                installs.append(pkg_ver)
                PackageManager(package).upgrade("--reinstall")
            elif GetFromInstalled(split_package(inst)[0]).name():
                print("[ {0}upgrading{1} ] --> {2}".format(
                    self.meta.color["YELLOW"], self.meta.color["ENDC"], inst))
                upgraded.append(pkg_ver)
                PackageManager(package).upgrade("--install-new")
            else:
                print("[ {0}installing{1} ] --> {2}".format(
                    self.meta.color["GREEN"], self.meta.color["ENDC"], inst))
                installs.append(pkg_ver)
                PackageManager(package).upgrade("--install-new")
        return [installs, upgraded]

    def checksums(self, install):
        """Checksums before install
        """
        check_md5(pkg_checksum(install, self.repo), self.tmp_path + install)

    def resolving_deps(self):
        """Return package dependencies
        """
        requires = []
        if (self.meta.rsl_deps in ["on", "ON"] and
                self.flag != "--resolve-off"):
            self.msg.resolving()
        for dep in self.packages:
            status(0.05)
            dependencies = []
            dependencies = Utils().dimensional_list(Dependencies(
                self.PACKAGES_TXT, self.repo, self.blacklist).binary(
                    dep, self.flag))
            requires += dependencies
            self.deps_dict[dep] = Utils().remove_dbs(dependencies)
        return Utils().remove_dbs(requires)

    def views(self, install, comp_sum):
        """Views packages
        """
        pkg_sum = uni_sum = upg_sum = 0
        # fix repositories align
        repo = self.repo + (" " * (6 - (len(self.repo))))
        for pkg, comp in zip(install, comp_sum):
            pkg_repo = split_package(pkg[:-4])
            if find_package(pkg[:-4], self.meta.pkg_path):
                pkg_sum += 1
                COLOR = self.meta.color["GREEN"]
            elif pkg_repo[0] == GetFromInstalled(pkg_repo[0]).name():
                COLOR = self.meta.color["YELLOW"]
                upg_sum += 1
            else:
                COLOR = self.meta.color["RED"]
                uni_sum += 1
            ver = GetFromInstalled(pkg_repo[0]).version()
            print("  {0}{1}{2}{3} {4}{5} {6}{7}{8}{9}{10}{11:>11}{12}".format(
                COLOR, pkg_repo[0] + ver, self.meta.color["ENDC"],
                " " * (23-len(pkg_repo[0] + ver)), pkg_repo[1],
                " " * (18-len(pkg_repo[1])), pkg_repo[2],
                " " * (8-len(pkg_repo[2])), pkg_repo[3],
                " " * (7-len(pkg_repo[3])), repo,
                comp, " K")).rstrip()
        return [pkg_sum, upg_sum, uni_sum]

    def top_view(self):
        """Print packages status bar
        """
        self.msg.template(78)
        print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
            "| Package", " " * 17,
            "New Version", " " * 8,
            "Arch", " " * 4,
            "Build", " " * 2,
            "Repos", " " * 10,
            "Size"))
        self.msg.template(78)

    def store(self, packages):
        """Store and return packages for install
        """
        dwn, install, comp_sum, uncomp_sum = ([] for i in range(4))
        # name = data[0]
        # location = data[1]
        # size = data[2]
        # unsize = data[3]
        for pkg in packages:
            for pk, loc, comp, uncomp in zip(self.data[0], self.data[1],
                                             self.data[2], self.data[3]):
                if (pk and pkg == split_package(pk)[0] and
                        pk not in install and
                        split_package(pk)[0] not in self.blacklist):
                    dwn.append("{0}{1}/{2}".format(self.mirror, loc, pk))
                    install.append(pk)
                    comp_sum.append(comp)
                    uncomp_sum.append(uncomp)
        if not install:
            for pkg in packages:
                for pk, loc, comp, uncomp in zip(self.data[0], self.data[1],
                                                 self.data[2], self.data[3]):
                    name = split_package(pk)[0]
                    if (pk and pkg in name and name not in self.blacklist):
                        dwn.append("{0}{1}/{2}".format(self.mirror, loc, pk))
                        install.append(pk)
                        comp_sum.append(comp)
                        uncomp_sum.append(uncomp)
        dwn.reverse()
        install.reverse()
        comp_sum.reverse()
        uncomp_sum.reverse()
        return [dwn, install, comp_sum, uncomp_sum]
