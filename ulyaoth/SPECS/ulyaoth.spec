%define ulyaothos sbagmeijer

Summary: Contains the repository file and GPG Key for the Ulyaoth Repository.
Name: ulyaoth
Version: 6.0.0
BuildArch: x86_64
URL: https://ulyaoth.com
Packager: Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
Release: 1.%{ulyaothos}
Source0: https://repos.ulyaoth.com/RPM-GPG-KEY-ulyaoth-20180607
Source1: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth/SOURCES/ulyaoth-%{ulyaothos}.repo
Source2: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth/SOURCES/COPYING
BuildRoot:  %{_tmppath}/ulyaoth-%{version}-%{release}-root-%(%{__id_u} -n)

License: GPLv3

Provides: ulyaoth
Obsoletes: ulyaoth <= 5.0.2

%description
Ulyaoth repository.

%install
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/licenses/ulyaoth

%{__install} -m 644 -p %{SOURCE0} \
   $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ulyaoth-20180607
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/ulyaoth.repo
%{__install} -m 644 -p %{SOURCE2} \
   $RPM_BUILD_ROOT/usr/share/licenses/ulyaoth/COPYING
   
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /usr/share/licenses/ulyaoth
%config(noreplace) /etc/yum.repos.d/ulyaoth.repo
/etc/pki/rpm-gpg/RPM-GPG-KEY-ulyaoth-20180607
/usr/share/licenses/ulyaoth/COPYING

%post
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using Ulyaoth repository!

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%changelog
* Fri May 10 2019 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 6.0.0-1
- Changed to single "RHEL" repository for all RHEL based distros.

* Wed Jun 13 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 5.0.2-1
- Changed repo files from tabs to spaces.

* Mon Jun 11 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 5.0.1-1
- Fixed all repository files to contain correct gpg key. (thank you Bent Terp)

* Thu Jun 7 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 5.0.0-1
- New domain name "repos.ulyaoth.com".
- New gpg2 key (sorry).
- Added date to gpg key in case key every has to change again it won't cause issue.

* Tue May 1 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 4.0.0-1
- Changed to a new gpg2 key.

* Thu Jan 4 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 3.0.1-1
- Support for Amazon Linux 2.

* Mon Nov 13 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 3.0.0-1
- Changed url locations to make repository more red hat / fedora alike.

* Mon Mar 20 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 2.0.0-1
- Changed repository domain to "repos.ulyaoth.io".

* Wed Oct 12 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.4-1
- Changed BuildArch.
- Fixed AmazonLinux download url.

* Sun May 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.3-1
- Changed domain back to repos.ulyaoth.net.

* Sun Apr 17 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.2-1
- Fixing "not signed" problem.

* Sat Apr 16 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.1-1
- Changed domain to repos.ulyaoth.asia.
- Added fallback to non SSL due to EL6 not supporting my ciphers.
- All rpms have been moved to Amazon S3.
- We are now using Cloudflare to speed up downloads.

* Sat Apr 2 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-1
- Changed to noarch to reduce rpms.

* Tue Nov 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.10-1
- Added Fedora 23 Support.

* Sat Oct 31 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.9-1
- Added Amazon Linux Support.

* Sun Oct 4 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.8-1
- Added Repository for Source rpms.

* Tue Aug 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.7-1
- Changed to a new gpg2 key that fixes the import problem.

* Sun Jun 28 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.6-1
- Added support for Scientific Linux 6 and 7.

* Sun May 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.5-1
- Changed EOL conversion to Unix to resolve a problem with CentOS unable to read the repo file.
- Changed debug on CentOS repo file to correct: [ulyaoth-debug].
- Also fixed the centos baseurl to have the correct CentOS instead of centos so it can find the files actually.

* Mon Apr 6 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.4-1
- Separating debug packages to own repository and disabled it by default. (same as Fedora or RHEL does it)

* Sat Mar 28 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.3-1
- Updating public GPG key to a new 4096 bits one.

* Fri Mar 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.2-1
- Support for Oracle Linux 6 and 7.

* Wed Mar 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.1-2
- Small fix to make spec file more clean.
- i386 Support.

* Wed Mar 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.1-1
- Support for CentOS 6, 7 and Fedora 22.

* Sat Oct 4 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.0-1
- Support for Fedora 21.

* Sun Aug 24 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 1.0.0-1
- Creating initial release.