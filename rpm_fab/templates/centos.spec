
Summary: %{descrition}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: x86_64
Vendor: CIRB <irisline@cirb.irisnet.be>
requires: python27

%description
%{descrition}

%prep

%build

%install
DESTINATION=$RPM_BUILD_ROOT/home/%{name}/%{name}
mkdir -p $DESTINATION
cp -r * $DESTINATION

cd $DESTINATION
make clean install

find . -name "*.pyc" -delete;
find . -name "*.pyo" -delete;

find ./bin/ -exec sed -i "s:$RPM_BUILD_ROOT::g" {} \;
find ./lib/python2.7/site-packages/ -exec sed -i "s:$RPM_BUILD_ROOT::g" {} \;

prelink --undo ./bin/python
prelink --undo ./bin/python2
prelink --undo ./bin/python2.7

%clean
rm -rf %{buildroot}

%post
cd /home/%{name}/%{name}
source /home/%{name}/env
make migrate

%files
%defattr(-,root,root)
/home/%{name}/%{name}
