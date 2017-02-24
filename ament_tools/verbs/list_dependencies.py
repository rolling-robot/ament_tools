# Copyright 2014 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_tools.helper import argparse_existing_dir
from ament_tools.packages import find_packages


def prepare_arguments(parser):
    parser.add_argument(
        'basepath',
        nargs='?',
        type=argparse_existing_dir,
        default=os.curdir,
        help='Base paths to recursively crawl for packages',
    )
    parser.add_argument(
        '--build-deps',
        action='store_true',
        help='Show build dependencies of a given package'
    )
    parser.add_argument(
        '--exec-deps',
        action='store_true',
        help='Show exec dependencies of a given package'
    )
    parser.add_argument(
        '--test-deps',
        action='store_true',
        help='Show test dependencies of a given package'
    )
    parser.add_argument(
        'package',
        metavar='PACKAGE',
        help='Package to process'
    )
    return parser


def main(options):
    lines = []
    packages = find_packages(options.basepath)
    for (path, package) in packages.items():
        if package.name == options.package:
            if options.build_deps:
                lines.extend(package.build_export_depends +
                             package.buildtool_export_depends +
                             package.build_depends +
                             package.buildtool_depends +
                             package.doc_depends)
            if options.exec_deps:
                lines.extend(package.exec_depends)
            if options.test_deps:
                lines.extend(package.test_depends)
            for line in lines:
                print(line)
            return
    print('No package with name {!r} found'.format(options.package))
    return -1

entry_point_data = dict(
    verb='list_dependencies',
    description='List names and relative paths of dependencies of packages',
    # Called for execution, given parsed arguments object
    main=main,
    # Called first to setup argparse, given argparse parser
    prepare_arguments=prepare_arguments,
)
