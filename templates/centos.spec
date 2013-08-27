
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
%setup -n %{name}-%{version} -n %{name}-%{version}


%build


%install
%{_topdir}/install.sh "%{_topdir}" "$RPM_BUILD_ROOT" "%{name}" "%{version}"


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
/usr/lib/%{name}
