
set -ex

RPM_BUILD_ROOT=$2

INSTALL_ROOT=$RPM_BUILD_ROOT/usr/lib/$RPM_NAME
mkdir -p $INSTALL_ROOT

cd $INSTALL_ROOT

make install
