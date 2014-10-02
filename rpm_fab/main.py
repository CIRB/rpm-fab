import os
import shutil
from exceptions import Exception

from fabric.api import local, run, put


# /etc/ssh/sshd_config
# Subsystem sftp internal-sftp
# service sshd restart
# yum install rpmdevtools


def rpm_fab():
    project_name = local("python setup.py --name", capture=True)
    project_version = local("python setup.py --version", capture=True)
    # project_description = local("python setup.py --description", capture=True)

    if os.path.exists('dist/'):
        local('rm -rf dist/')

    local("python setup.py sdist", capture=True)

    project_sources = local("echo dist/*.tar.gz", capture=True)
    if not os.path.exists(project_sources):
        raise Exception("failed to archive sources")

    build_root = run('mktemp -d')

    root_sources = '{0}/SOURCES/'.format(build_root)
    run('mkdir {0}'.format(root_sources))
    put(project_sources, root_sources)

    root_specs = '{0}/SPECS/'.format(build_root)
    run('mkdir {0}'.format(root_specs))
    put('templates/centos.spec', root_specs)

    put('templates/install.sh', build_root)

    run_build(
        build_root=build_root,
        project_name=project_name,
        project_version=project_version,
    )

    print('Allright !! RPM has been build !')

    bring_rpm_back(build_root)


def bring_rpm_back(dest):
    archs = run('ls {0}/RPMS/'.format(dest))

    if len(archs) != 1:
        raise Exception('rpm not found at {0}'.format(dest))

    rpms_path = '{0}/RPMS/{1}'.format(dest, archs[0])

    shutil.copy('{0}/{1}-{2}-1.x86_64.rpm'.format(
        rpms_path,
        project_infos['name'],
        project_infos['version']
    ), 'dist')


def run_build(**kwargs):
    run(
        'rpmbuild'
        ' --define "name {project_name}"'
        ' --define "version {project_version}"'
        ' --define "release 1"'
        ' --define="_topdir {build_root}"'
        ' -bb {0}/SPECS/centos.spec'
        .format(**kwargs))
