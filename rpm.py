import sys
from fabric.tasks import execute

from rpm_fab.main import rpm

try:
    execute(
        rpm,
        hosts=sys.argv[1:],
    )
    rpm()
except (EOFError, TypeError) as err:
    print(err)
    sys.exit(1)
