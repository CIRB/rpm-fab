import os

from fabric.api import local, sudo, run as remote_run, put as remote_put, get as remote_get
from fabric.contrib.project import rsync_project
from fabric.state import env

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# /etc/ssh/sshd_config
# Subsystem sftp internal-sftp
# service sshd restart
# yum install rpmdevtools


def run(*args, **kwargs):
    if env.hosts:
        return remote_run(*args, **kwargs)
    else:
        kwargs['capture'] = True
        return local(*args, **kwargs)


def put(src, dest, *args, **kwargs):
    if env.hosts:
        return remote_put(src, dest, *args, **kwargs)
    else:
        return local('cp {0} {1}'.format(src, dest))


def get(src, dest, *args, **kwargs):
    if env.hosts:
        return remote_get(src, dest, *args, **kwargs)
    else:
        return local('cp {0} {1}'.format(src, dest))


def sync(*args, **kwargs):
    if env.hosts:
        return rsync_project(*args, **kwargs)
    else:
        cmd = 'rsync -av {local_dir} {remote_dir}'.format(**kwargs)
        if 'exclude' in kwargs:
            cmd += ' '.join(
                [' --exclude ' + excl_dir for excl_dir in kwargs['exclude']]
            )

        return local(cmd)


def rpm_build():
    project_name = local("python setup.py --name", capture=True)
    project_version = local("python setup.py --version", capture=True)

    build_root = run('mktemp -d')

    root_sources = '{0}/BUILD/'.format(build_root)
    run('mkdir {0}'.format(root_sources))

    sync(
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

    run('rm -rf {0}'.format(build_root))


def rpm_install():
    project_name = local("python setup.py --name", capture=True)
    rpm_path = put('dist/*.rpm', '/tmp')
    sudo('yum remove  -y {}'.format(project_name))
    sudo('yum install -y {}'.format(rpm_path[0]))


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
