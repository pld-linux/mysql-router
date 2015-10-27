# TODO
# - fix libdir
# - fix shared libs SONAME
Summary:	MySQL Router
Name:		mysql-router
Version:	2.0.2
Release:	0.1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://dev.mysql.com/get/Downloads/MySQL-Router/%{name}-%{version}.tar.gz
# Source0-md5:	de7f65e9a61f939e0c4bab7c251d9763
URL:		http://dev.mysql.com/doc/mysql-router/en/
BuildRequires:	cmake >= 2.8.9
BuildRequires:	doxygen
BuildRequires:	glibc-devel >= 6:2.17
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	mysql-devel >= 5.5
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

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/mysqlrouter

# TODO: fix build instead
%define	_libdir	%{_prefix}/lib

# no -devel yet
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/mysql/mysqlrouter
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmysqlharness.a
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmysqlharness.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmysqlrouter.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt License.txt
%attr(755,root,root) %{_bindir}/mysqlrouter
%attr(755,root,root) %{_libdir}/libmysqlharness.so.0
%attr(755,root,root) %{_libdir}/libmysqlrouter.so.1
%dir %{_libdir}/mysqlrouter
%attr(755,root,root) %{_libdir}/mysqlrouter/fabric_cache.so
%attr(755,root,root) %{_libdir}/mysqlrouter/keepalive.so
%attr(755,root,root) %{_libdir}/mysqlrouter/logger.so
%attr(755,root,root) %{_libdir}/mysqlrouter/routing.so
