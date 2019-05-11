
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
Name:       ulyaoth-tomcat8.5
Version:    8.5.40
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-8/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.logrotate
BuildRoot:  %{_tmppath}/tomcat-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: tomcat
Provides: apache-tomcat
Provides: ulyaoth-tomcat
Provides: ulyaoth-tomcat8.5

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

Thank you for using ulyaoth-tomcat8.5!

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
* Sat May 11 2019 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 8.5.40-1
- Updating to Tomcat 8.5.40.

* Mon Nov 12 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 8.5.35-1
- Updating to Tomcat 8.5.35.

* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 8.5.34-1
- Updating to Tomcat 8.5.34.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 8.5.31-1
- Updating to Tomcat 8.5.31.

* Fri Jan 5 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 8.5.24-1
- Updating to Tomcat 8.5.24.

* Wed Nov 15 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 8.5.23-1
- Updating to Tomcat 8.5.23.

* Sat Jul 1 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 8.5.16-1
- Updating to Tomcat 8.5.16.

* Sat May 20 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.15-1
- Updating to Tomcat 8.5.15.

* Sat Apr 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.14-1
- Updating to Tomcat 8.5.14.

* Sat Apr 8 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.13-1
- Updating to Tomcat 8.5.13.

* Fri Mar 17 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.12-1
- Updating to Tomcat 8.5.12.

* Mon Feb 13 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.11-1
- Updating to Tomcat 8.5.11.

* Sun Nov 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.8-1
- Updating to Tomcat 8.5.8.

* Sat Oct 15 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.6-1
- Updating to Tomcat 8.5.6.

* Sat Sep 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.5-1
- Updating to 8.5.5.

* Tue Jul 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.4-1
- Updating to 8.5.4.

* Thu Jun 16 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 8.5.3-1
- Initial release for Tomcat 8.5 rpms.
