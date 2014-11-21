
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
%{descrition}

%prep

%build
make install

%install
rm -rf $RPM_BUILD_ROOT || true
mkdir -p $RPM_BUILD_ROOT/usr/lib/%{name}
cp -r * $RPM_BUILD_ROOT/usr/lib/%{name}

%clean
rm -rf %{buildroot}

%post
make migrate

%files
%defattr(-,root,root)
/usr/lib/%{name}
