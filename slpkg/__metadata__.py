#!/usr/bin/python
# -*- coding: utf-8 -*-

# __metadata__.py file is part of slpkg.

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


def remove_repositories(repositories, default_repositories):
    """
    Remove no default repositories
    """
    repos = []
    for repo in repositories:
        if repo in default_repositories:
            repos.append(repo)
    return repos


def update_repositories(repositories, conf_path):
    """
    Upadate with user custom repositories
    """
    repo_file = "{0}custom-repositories".format(conf_path)
    if os.path.isfile(repo_file):
        f = open(repo_file, "r")
        repositories_list = f.read()
        f.close()
        for line in repositories_list.splitlines():
            line = line.lstrip()
            if line and not line.startswith("#"):
                repositories.append(line.split()[0])
    return repositories


def grab_sub_repo(repositories, repos):
    """
    Grab SUB_REPOSITORY
    """
    for i, repo in enumerate(repositories):
        if repos in repo:
            sub = repositories[i].replace(repos, "")
            repositories[i] = repos
            return sub


def select_slack_release(slack_rel):
    """
    Warning message if Slackware release not defined or
    defined wrong
    """
    if slack_rel not in ["stable", "current"]:
        return "FAULT"
    return slack_rel


class MetaData(object):

    __all__ = "slpkg"
    __author__ = "dslackw"
    __version_info__ = (3, 0, 1)
    __version__ = "{0}.{1}.{2}".format(*__version_info__)
    __license__ = "GNU General Public License v3 (GPLv3)"
    __email__ = "d.zlatanidis@gmail.com"

    # Default Slackware release
    slack_rel = "stable"

    # Configuration path
    conf_path = "/etc/{0}/".format(__all__)

    # tmp paths
    tmp = "/tmp/"
    tmp_path = "{0}{1}/".format(tmp, __all__)

    # Default configuration values
    _conf_slpkg = {
        "RELEASE": "stable",
        "REPOSITORIES": ["slack", "sbo", "rlw", "alien",
                         "slacky", "studio", "slackr", "slonly",
                         "ktown{latest}", "multi", "slacke{18}",
                         "salix", "slackl", "rested", "msb{1.10}"],
        "BUILD_PATH": "/tmp/slpkg/build/",
        "PACKAGES": "/tmp/slpkg/packages/",
        "PATCHES": "/tmp/slpkg/patches/",
        "CHECKMD5": "on",
        "DEL_ALL": "on",
        "DEL_BUILD": "off",
        "SBO_BUILD_LOG": "on",
        "MAKEFLAGS": "off",
        "DEFAULT_ANSWER": "n",
        "REMOVE_DEPS_ANSWER": "n",
        "SKIP_UNST": "n",
        "RSL_DEPS": "on",
        "DEL_DEPS": "off",
        "USE_COLORS": "on",
        "DOWNDER": "wget",
        "DOWNDER_OPTIONS": "-c -N",
        "SLACKPKG_LOG": "on",
        "ONLY_INSTALLED": "off",
        "PRG_BAR": "on",
        "EDITOR": "nano"
    }

    default_repositories = ["slack", "sbo", "rlw", "alien", "slacky", "studio",
                            "slackr", "slonly", "ktown", "multi", "slacke",
                            "salix", "slackl", "rested", "msb"]

    # read value from configuration file
    repositories = []
    for files in ["slpkg.conf", "repositories.conf"]:
        if os.path.isfile("%s%s" % (conf_path, files)):
            f = open("%s%s" % (conf_path, files), "r")
            conf = f.read()
            f.close()
            for line in conf.splitlines():
                line = line.lstrip()
                if line and not line.startswith("#"):
                    if files == "slpkg.conf":
                        _conf_slpkg[line.split("=")[0]] = line.split("=")[1]
                    elif files == "repositories.conf":
                        repositories.append(line)
    # Set values from configuration file
    slack_rel = _conf_slpkg["RELEASE"]
    build_path = _conf_slpkg["BUILD_PATH"]
    slpkg_tmp_packages = _conf_slpkg["PACKAGES"]
    slpkg_tmp_patches = _conf_slpkg["PATCHES"]
    checkmd5 = _conf_slpkg["CHECKMD5"]
    del_all = _conf_slpkg["DEL_ALL"]
    del_build = _conf_slpkg["DEL_BUILD"]
    sbo_build_log = _conf_slpkg["SBO_BUILD_LOG"]
    makeflags = _conf_slpkg["MAKEFLAGS"]
    default_answer = _conf_slpkg["DEFAULT_ANSWER"]
    remove_deps_answer = _conf_slpkg["REMOVE_DEPS_ANSWER"]
    skip_unst = _conf_slpkg["SKIP_UNST"]
    rsl_deps = _conf_slpkg["RSL_DEPS"]
    del_deps = _conf_slpkg["DEL_DEPS"]
    use_colors = _conf_slpkg["USE_COLORS"]
    downder = _conf_slpkg["DOWNDER"]
    downder_options = _conf_slpkg["DOWNDER_OPTIONS"]
    slackpkg_log = _conf_slpkg["SLACKPKG_LOG"]
    only_installed = _conf_slpkg["ONLY_INSTALLED"]
    prg_bar = _conf_slpkg["PRG_BAR"]
    editor = _conf_slpkg["EDITOR"]

    # Remove any gaps
    repositories = [repo.strip() for repo in repositories]

    # Check Slackware release
    slack_rel = select_slack_release(slack_rel)

    # Grap sub repositories
    ktown_kde_repo = grab_sub_repo(repositories, "ktown")
    slacke_sub_repo = grab_sub_repo(repositories, "slacke")
    msb_sub_repo = grab_sub_repo(repositories, "msb")

    # remove no default repositories
    repositories = remove_repositories(repositories, default_repositories)

    # add custom repositories
    update_repositories(repositories, conf_path)

    color = {
        "RED": "\x1b[31m",
        "GREEN": "\x1b[32m",
        "YELLOW": "\x1b[33m",
        "CYAN": "\x1b[36m",
        "GREY": "\x1b[38;5;247m",
        "ENDC": "\x1b[0m"
    }

    if use_colors in ["off", "OFF"]:
        color = {
            "RED": "",
            "GREEN": "",
            "YELLOW": "",
            "CYAN": "",
            "GREY": "",
            "ENDC": ""
        }

    CHECKSUMS_link = ("https://raw.githubusercontent.com/{0}/{1}/"
                      "master/CHECKSUMS.md5".format(__author__, __all__))

    # file spacer
    sp = "-"

    # current path
    try:
        path = os.getcwd() + "/"
    except OSError:
        path = tmp_path

    # library path
    lib_path = "/var/lib/slpkg/"

    # log path
    log_path = "/var/log/slpkg/"

    # packages log files path
    pkg_path = "/var/log/packages/"

    # slackpkg lib path
    slackpkg_lib_path = "/var/lib/slackpkg/"

    # computer architecture
    arch = os.uname()[4]

    # get sbo OUTPUT enviroment variable
    try:
        output = os.environ["OUTPUT"]
    except KeyError:
        output = tmp
    if not output.endswith("/"):
        output += "/"
