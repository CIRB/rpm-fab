
set -ex

TOP_DIR=$1
RPM_BUILD_ROOT=$2
RPM_NAME=$3
RPM_VERSION=$4

INSTALL_ROOT=$RPM_BUILD_ROOT/usr/lib/$RPM_NAME
mkdir -p $INSTALL_ROOT

cp $TOP_DIR/buildout.cfg $INSTALL_ROOT
cd $INSTALL_ROOT

python $TOP_DIR/bootstrap.py
bin/buildout app:eggs=rpm_fab app:find-links=$TOP_DIR
rm $INSTALL_ROOT/.installed.cfg
rm $INSTALL_ROOT/buildout.cfg
rm $INSTALL_ROOT/bin/buildout
rm -r $INSTALL_ROOT/parts
rm -r $INSTALL_ROOT/develop-eggs





# rpm_:egg=$RPM_NAME \
#   python:url=file://$TOP_DIR/SOURCES/$RPM_NAME-$RPM_VERSION.tar.gz
#bin/buildout setup $TOP_DIR/BUILD/$RPM_NAME/setup.py install



# ENV_ROOT=$INSTALL_ROOT/lib/python/

# echo "import os, site; site.addsitedir(os.path.expanduser('$ENV_ROOT/lib/python/'))" > $ENV_ROOT/altinstall.pth
# export PYTHONPATH=$ENV_ROOT

# python setup.py install \
#     --optimize 1 \
#     --home=$INSTALL_ROOT

# sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $ENV_ROOT/altinstall.pth
