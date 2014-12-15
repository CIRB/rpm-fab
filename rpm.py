#!/usr/bin/env python2

import sys
import argparse
from fabric.tasks import execute
from fabric.state import env

from rpm_fab.main import rpm_build, rpm_install

parser = argparse.ArgumentParser()
parser.add_argument('action', choices=('build', 'install'), help='What to do')
parser.add_argument('-H', '--host', required=False, help='Where to do')

args = parser.parse_args()
env.hosts = [args.host] if args.host else None

try:
    action = args.action
    if action == 'build':
        execute(rpm_build)
    elif action == 'install':
        execute(rpm_install)
except (EOFError, TypeError) as err:
    print(err)
    sys.exit(1)
