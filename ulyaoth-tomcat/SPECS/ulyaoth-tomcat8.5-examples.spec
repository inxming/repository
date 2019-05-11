
%define __jar_repack %{nil}
%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine
Name:       ulyaoth-tomcat8.5-examples
Version:    8.5.40
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-8/v%{version}/bin/apache-tomcat-%{version}.tar.gz
BuildRoot:  %{_tmppath}/tomcat-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-tomcat8.5

Provides: tomcat-examples
Provides: apache-tomcat-examples
Provides: ulyaoth-tomcat-examples
Provides: ulyaoth-tomcat8.5-examples

%description
The package contains the official Apache Tomcat "webapps/examples" and "webapps/ROOT" directories.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Delete all files except webapp admin
%{__rm} -rf %{buildroot}/%{tomcat_home}/bin
%{__rm} -rf %{buildroot}/%{tomcat_home}/conf
%{__rm} -rf %{buildroot}/%{tomcat_home}/lib
%{__rm} -rf %{buildroot}/%{tomcat_home}/LICENSE
%{__rm} -rf %{buildroot}/%{tomcat_home}/NOTICE
%{__rm} -rf %{buildroot}/%{tomcat_home}/RELEASE-NOTES
%{__rm} -rf %{buildroot}/%{tomcat_home}/RUNNING.txt
%{__rm} -rf %{buildroot}/%{tomcat_home}/BUILDING.txt
%{__rm} -rf %{buildroot}/%{tomcat_home}/CONTRIBUTING.md
%{__rm} -rf %{buildroot}/%{tomcat_home}/README.md
%{__rm} -rf %{buildroot}/%{tomcat_home}/temp
%{__rm} -rf %{buildroot}/%{tomcat_home}/work
%{__rm} -rf %{buildroot}/%{tomcat_home}/logs
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/docs
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/host-manager
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/manager

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%dir %{tomcat_home}/webapps/examples
%dir %{tomcat_home}/webapps/ROOT
%{tomcat_home}/webapps/examples/*
%{tomcat_home}/webapps/ROOT/*

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-tomcat8.5-examples!

Please find the official documentation for tomcat here:
* https://tomcat.apache.org/

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

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
