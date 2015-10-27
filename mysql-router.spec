Summary:	MySQL Router
Name:		mysql-router
Version:	2.0.2
Release:	0.1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://dev.mysql.com/get/Downloads/MySQL-Router/%{name}-%{version}.tar.gz
# Source0-md5:	de7f65e9a61f939e0c4bab7c251d9763
URL:		http://dev.mysql.com/doc/mysql-router/en/
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL Router is lightweight middleware that provides transparent
routing between your application and any backend MySQL Servers. It can
be used for a wide variety of use cases, such as providing high
availability and scalability by effectively routing database traffic
to appropriate backend MySQL Servers. The pluggable architecture also
enables developers to extend MySQL Router for custom use cases.

%prep
%setup -q

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
