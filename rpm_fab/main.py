import os
from exceptions import Exception

from fabric.api import local, run, put, get
from fabric.contrib.project import rsync_project

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# /etc/ssh/sshd_config
# Subsystem sftp internal-sftp
# service sshd restart
# yum install rpmdevtools


def rpm_build():
    project_name = local("python setup.py --name", capture=True)
    project_version = local("python setup.py --version", capture=True)

    build_root = run('mktemp -d')

    root_sources = '{0}/BUILD/'.format(build_root)
    run('mkdir {0}'.format(root_sources))
    # put('.', root_sources)

    rsync_project(
        local_dir='.',
        remote_dir=root_sources,
        exclude=['.git', 'bin', 'lib', 'dist']
    )

    root_specs = '{0}/SPECS/'.format(build_root)
    run('mkdir {0}'.format(root_specs))
    put('{0}/templates/centos.spec'.format(ROOT_DIR), root_specs)

    run_build(
        build_root=build_root,
        project_name=project_name,
        project_version=project_version,
    )

    print('Allright !! RPM has been build !')

    dist_path = 'dist'
    local("rm -rf {}".format(dist_path))
    local("mkdir {}".format(dist_path))

    bring_rpm_back(build_root, dist_path, project_name, project_version)


def rpm_install():
    rpm_path = put('dist/*.rpm', '/tmp')
    run('yum install -y {}'.format(rpm_path[0]))


def bring_rpm_back(build_root, dest, name, version):
    arch = 'x86_64'
    rpm_path = (
        '{build_root}/RPMS/{arch}/'
        '{name}-{version}-1.{arch}.rpm').format(
            build_root=build_root,
            arch=arch,
            name=name,
            version=version
        )

    return get(rpm_path, dest)


def run_build(**kwargs):
    run(
        'rpmbuild'
        ' --define "name {project_name}"'
        ' --define "version {project_version}"'
        ' --define "release 1"'
        ' --define="_topdir {build_root}"'
        ' -bb {build_root}/SPECS/centos.spec'
        .format(**kwargs))
