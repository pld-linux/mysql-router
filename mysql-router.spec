# TODO
# - fix shared libs SONAME
# - user (use mysql user like upstream .spec does)
# - file/dir permissions (configs will likely contain passwords?)
# - services (systemd, init.d)
# - logrotate
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
%cmake \
	-DINSTALL_LAYOUT=RPM \
	-DINSTALL_LIBDIR=%{_libdir} \
	-DWITH_STATIC=no \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_localstatedir}/{log,run}/mysqlrouter \
	$RPM_BUILD_ROOT{%{systemdunitdir},%{systemdtmpfilesdir},%{_sysconfdir}/mysqlrouter}

cp -p build/packaging/rpm-oel/mysqlrouter.service $RPM_BUILD_ROOT%{systemdunitdir}/mysqlrouter.service
cp -p build/packaging/rpm-oel/mysqlrouter.tmpfiles.d $RPM_BUILD_ROOT%{systemdtmpfilesdir}/mysqlrouter.conf
cp -p build/packaging/rpm-oel/mysqlrouter.ini $RPM_BUILD_ROOT%{_sysconfdir}/mysqlrouter/mysqlrouter.ini

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
%dir %{_sysconfdir}/mysqlrouter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysqlrouter/mysqlrouter.ini
%attr(755,root,root) %{_sbindir}/mysqlrouter
%attr(755,root,root) %{_libdir}/libmysqlharness.so.0
%attr(755,root,root) %{_libdir}/libmysqlrouter.so.1
%dir %{_libdir}/mysqlrouter
%attr(755,root,root) %{_libdir}/mysqlrouter/fabric_cache.so
%attr(755,root,root) %{_libdir}/mysqlrouter/keepalive.so
%attr(755,root,root) %{_libdir}/mysqlrouter/logger.so
%attr(755,root,root) %{_libdir}/mysqlrouter/routing.so
%{systemdunitdir}/mysqlrouter.service
%{systemdtmpfilesdir}/mysqlrouter.conf
%dir %{_localstatedir}/run/mysqlrouter
%dir %{_localstatedir}/log/mysqlrouter
