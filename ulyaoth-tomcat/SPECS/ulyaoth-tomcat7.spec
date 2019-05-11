
%define __jar_repack %{nil}
%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary:    Apache Servlet/JSP Engine
Name:       ulyaoth-tomcat7
Version:    7.0.94
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-7/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1:	https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.logrotate
BuildRoot:  %{_tmppath}/tomcat-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: tomcat
Provides: apache-tomcat
Provides: ulyaoth-tomcat
Provides: ulyaoth-tomcat7

%description
Apache Tomcat is an open source software implementation of the Java Servlet and JavaServer Pages technologies. The Java Servlet and JavaServer Pages specifications are developed under the Java Community Process.

Apache Tomcat is developed in an open and participatory environment and released under the Apache License version 2. Apache Tomcat is intended to be a collaboration of the best-of-breed developers from around the world. We invite you to participate in this open development project. To learn more about getting involved, click here.

Apache Tomcat powers numerous large-scale, mission-critical web applications across a diverse range of industries and organizations. Some of these users and their stories are listed on the PoweredBy wiki page.

Apache Tomcat, Tomcat, Apache, the Apache feather, and the Apache Tomcat project logo are trademarks of the Apache Software Foundation.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{tomcat_home}/logs
install -d -m 755 %{buildroot}/var/log/tomcat/
cd %{buildroot}/%{tomcat_home}/
ln -s /var/log/tomcat/ logs
cd -

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/tomcat.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/tomcat
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/tomcat

# Clean webapps
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/*
   
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd --comment "Tomcat Daemon User" --shell /bin/bash -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%{tomcat_home}/*
%dir %{tomcat_home}
%dir %{_localstatedir}/log/tomcat
%config(noreplace) %{tomcat_home}/conf/web.xml
%config(noreplace) %{tomcat_home}/conf/tomcat-users.xml
%config(noreplace) %{tomcat_home}/conf/server.xml
%config(noreplace) %{tomcat_home}/conf/logging.properties
%config(noreplace) %{tomcat_home}/conf/context.xml
%config(noreplace) %{tomcat_home}/conf/catalina.properties
%config(noreplace) %{tomcat_home}/conf/catalina.policy

%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/logrotate.d/tomcat
%if %{use_systemd}
%{_unitdir}/tomcat.service
%else
%{_initrddir}/tomcat
%endif


%post
# Register the tomcat service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset tomcat.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add tomcat
%endif

cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-tomcat7!

Please find the official documentation for tomcat here:
* https://tomcat.apache.org/

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable tomcat.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop tomcat.service >/dev/null 2>&1 ||:
%else
    /sbin/service tomcat stop > /dev/null 2>&1
    /sbin/chkconfig --del tomcat
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service tomcat status  >/dev/null 2>&1 || exit 0
fi

%changelog
* Sat May 11 2019 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 7.0.94-1
- Updated to Tomcat 7.0.94.

* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 7.0.91-1
- Updated to Tomcat 7.0.91.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.0.88-1
- Updated to Tomcat 7.0.88.

* Wed Nov 15 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.0.82-1
- Updated to Tomcat 7.0.82.

* Tue Jul 4 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 7.0.79-1
- Updated to Tomcat 7.0.79.

* Sat May 20 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.78-1
- Updated to Tomcat 7.0.78.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.77-1
- Updated to Tomcat 7.0.77.

* Fri Mar 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.76-1
- Updated to Tomcat 7.0.76.

* Mon Feb 13 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.75-1
- Updated to Tomcat 7.0.75.

* Sat Nov 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.73-1
- Updated to Tomcat 7.0.73.

* Sat Oct 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.72-1
- Updated to Tomcat 7.0.72.

* Wed Jun 22 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.70-1
- Updated to Tomcat 7.0.70.

* Tue Apr 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.69-1
- Updated to Tomcat 7.0.69.

* Sat Apr 9 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.68-1
- Updated to Tomcat 7.0.68.

* Sun Dec 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.67-1
- Updated to Tomcat 7.0.67.

* Sat Oct 24 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.65-1
- Updated to Tomcat 7.0.65.

* Sun Aug 30 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.64-1
- Updated to Tomcat 7.0.64.

* Thu Jul 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.63-1
- Updated to Tomcat 7.0.63.

* Fri May 15 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.62-1
- Updated to Tomcat 7.0.62.

* Sat Apr 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.61-1
- Updated to Tomcat 7.0.61.

* Fri Mar 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-3
- Support for Oracle Linux 6 & 7.

* Wed Mar 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-2
- Removal of some things from spec file.
- Support for Fedora 22 and CentOS 6 & 7.
- i386 Support.

* Fri Feb 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-1
- Updated to Tomcat 7.0.59.

* Tue Nov 18 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.57-1
- New rpms contain from now on a empty webapps dir, see new packages for admin interface.
- Updated to Tomcat 7.0.57.

* Wed Oct 8 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.56-1
- Updated to Tomcat 7.0.56.

* Sat Oct 4 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.55-1
- Support for Fedora 21.

* Tue Sep 16 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.55-1
- Creating spec for Tomcat 7.0.55.
- Used nginx spec file as basis.
- Original spec taken from: https://github.com/nmilford/rpm-tomcat7/blob/master/tomcat7.spec
- Changing structure slightly
