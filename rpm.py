import sys
import argparse
from fabric.tasks import execute

from rpm_fab.main import rpm_build, rpm_install

parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument('-H', '--host', help='increase output verbosity')

args = parser.parse_args()

try:
    action = args.action
    if action == 'build':
        execute(
            rpm_build,
            hosts=[args.host],
        )
    if action == 'install':
        execute(
            rpm_install,
            hosts=[args.host],
        )
except (EOFError, TypeError) as err:
    print(err)
    sys.exit(1)
