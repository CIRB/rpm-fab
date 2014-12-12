#!/usr/bin/env python2

import sys
import argparse
from fabric.tasks import execute

from rpm_fab.main import rpm_build, rpm_install

parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument('-H', '--host', help='increase output verbosity', required=False)

args = parser.parse_args()
hosts = [args.host or 'localhost']

try:
    action = args.action
    if action == 'build':
        execute(
            rpm_build,
            hosts=hosts
        )
    elif action == 'install':
        execute(
            rpm_install,
            hosts=hosts
        )
    else:
        print "action should be 'build' or 'install'"
except (EOFError, TypeError) as err:
    print(err)
    sys.exit(1)
