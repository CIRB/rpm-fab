
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

%description
UNKNOWN

%prep
tar xvzf %{_sourcedir}/%{name}-%{version}.tar.gz

%setup -n %{name}-%{version} -n %{name}-%{version}

%build
rm -rf $RPM_BUILD_ROOT || true
mkdir -p $RPM_BUILD_ROOT/usr/lib/%{name}
cp -r * $RPM_BUILD_ROOT/usr/lib/%{name}

%install
cd $RPM_BUILD_ROOT/usr/lib/%{name}
make install

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
/usr/lib/%{name}
