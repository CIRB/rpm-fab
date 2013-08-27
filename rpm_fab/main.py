import os
import stat
import tempfile
import shutil
from string import Template
from exceptions import Exception

from fabric.api import local, run

project_infos = {}

def rpm_fab():
    project_infos['name'] = local("python setup.py --name", capture=True)
    project_infos['version'] = local("python setup.py --version", capture=True)
    project_infos['description'] = local("python setup.py --description", capture=True)

    if os.path.exists('dist/'):
        shutil.rmtree('dist/')

    local("python setup.py sdist", capture=True)
    local("python setup.py bdist_egg", capture=True)

    project_infos['source_archive'] = local("echo dist/*.tar.gz", capture=True)
    project_infos['source_egg'] = local("echo dist/*.egg", capture=True)
    if not os.path.exists(project_infos['source_archive']):
        raise Exception("failed to archive source, try 'python setup.py sdist'")

    rpm_build_root = create_rpm_build_root()

    print('building project in {0}'.format(rpm_build_root))
    print('with infos {0}'.format(project_infos))

    root_sources = '{0}/SOURCES'.format(rpm_build_root)
    copy_sources(root_sources)
    copy_egg(rpm_build_root)

    root_specs = '{0}/SPECS'.format(rpm_build_root)
    copy_centos_spec(root_specs)

    copy_install_script(rpm_build_root)

    run_build(rpm_build_root)

    print('Allright !! RPM has been build !')

    bring_rpm_back(rpm_build_root)

    cleaning(rpm_build_root)


def create_rpm_build_root():
    rpm_build_root = tempfile.mkdtemp()
    return rpm_build_root


def copy_install_script(dest):
    shutil.copy('templates/install.sh', dest)
    shutil.copy('templates/buildout.cfg', dest)
    shutil.copy('templates/bootstrap.py', dest)

    install_script = '{0}/install.sh'.format(dest)

    st = os.stat(install_script)
    os.chmod(install_script, st.st_mode | stat.S_IEXEC)


def copy_sources(dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    shutil.copy(project_infos['source_archive'], dest)

def copy_egg(dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    shutil.copy(project_infos['source_egg'], dest)


def copy_centos_spec(dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    shutil.copy('templates/centos.spec', dest)


def install_sysvinit():
    template = Template(os.open("gunicorn_sysvinit.tmpl").read())
    content = template.substitute()


def bring_rpm_back(dest):
    archs = os.listdir('{0}/RPMS/'.format(dest))

    if len(archs) != 1:
        raise Exception('rpm not found at {0}'.format(rpms_path))

    rpms_path = '{0}/RPMS/{1}'.format(dest, archs[0])

    shutil.copy('{0}/{1}-{2}-1.x86_64.rpm'.format(
        rpms_path,
        project_infos['name'],
        project_infos['version']
    ), 'dist')


def run_build(rpm_build_root):
    local('rpmbuild'
            ' --define "name {name}"'
            ' --define "version {version}"'
            ' --define "release 1"'
            ' --define="_topdir {0}"'
            ' -bb {0}/SPECS/centos.spec'
            .format(rpm_build_root, **project_infos))


def cleaning(dest):
    shutil.rmtree(dest)


