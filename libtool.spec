%undefine _hardened_build
%global  gcc_major  7.3.0

Name:    libtool
Version: 2.4.6
Release: 33
License: GPLv2+ and LGPLv2+ and GFDL
Summary: The GNU Portable Library Tool
URL:     http://www.gnu.org/software/libtool/
Source0:  http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.xz

Patch0:     libtool-2.4.5-rpath.patch
Patch1:     libtool-2.4.6-am-1.16-test.patch
Patch6000:  libtool-exit-verbosely-for-fatal-configure-problems.patch
Patch6001:  libtool-fix-GCC-linking-with-specs.patch

Requires: gcc(major),autoconf, automake, sed, tar, findutils

BuildRequires: texinfo autoconf automake help2man gdb
BuildRequires: libstdc++-devel gcc-gfortran gcc gcc-c++

%description
GNU libtool is a generic library support script.
Libtool hides the complexity of using shared libraries behind a consistent, portable interface.

%package ltdl
Summary:  Runtime libraries for GNU Libtool Dynamic Module Loader
Provides: %{name}-libs = %{version}-%{release}

%description ltdl
The libtool-ltdl package contains the GNU Libtool Dynamic Module Loader, a
library that provides a consistent, portable interface which simplifies the
process of using dynamic modules.

%package   devel
Summary:   Tools needed for development using the GNU Libtool Dynamic Module Loader
License:   LGPLv2+
Requires:  automake
Requires:  %{name}-ltdl = %{version}-%{release}
Provides:  %{name}-ltdl-devel
Obsoletes: %{name}-ltdl-devel

%description devel
Static libraries and header files for development with ltdl.

%package_help

%prep
%autosetup -n libtool-%{version} -p1

autoreconf -v

%build
export CC=gcc
export CXX=g++
export F77=gfortran
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export FFLAGS=$(echo "$RPM_OPT_FLAGS -I/usr/lib64/gfortran/modules"| sed 's/-fstack-protector-strong/ /g')
export FCFLAGS=$(echo "$RPM_OPT_FLAGS -I/usr/lib64/gfortran/modules"| sed 's/-fstack-protector-strong/ /g')
%ifarch x86_64
export FFLAGS="$RPM_OPT_FLAGS -fPIE"
export FCFLAGS="$RPM_OPT_FLAGS -fPIE"
%endif

%configure

%make_build CUSTOM_LTDL_CFLAGS="%_hardening_cflags" CUSTOM_LTDL_LDFLAGS="%_hardening_ldflags"

%check
make check VERBOSE=yes

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/libltdl.{a,la}

%files
%license COPYING
%doc AUTHORS NEWS THANKS TODO ChangeLog*
%{_bindir}/libtool
%{_bindir}/libtoolize
%{_datadir}/aclocal/*.m4
%dir %{_datadir}/libtool
%{_datadir}/libtool/build-aux

%files ltdl
%license libltdl/COPYING.LIB
%{_libdir}/libltdl.so.*

%files devel
%license libltdl/COPYING.LIB
%doc libltdl/README
%{_datadir}/libtool
%exclude %{_datadir}/libtool/build-aux
%{_includedir}/ltdl.h
%{_includedir}/libltdl
%{_libdir}/libltdl.so

%files help
%doc README
%{_infodir}/libtool.info*.gz
%{_mandir}/man1/libtool.1*
%{_mandir}/man1/libtoolize.1*


%changelog
* Thu Aug 20 2020 tianwei <tianwei12@huawei.com> - 2.4.6-33
- fixbug testcase fail for gfortan

* Thu Mar 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.6-32
- add necessary BuildRequires

* Mon Jan 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.6-31
- fixbug in wrong dependency of kernel-devel

* Wed Jan 8 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.6-30
- format patches

* Thu Sep 5 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.4.6-29
- Package init

* Sun Feb 24 2019 zoujing <zoujing13@huawei.com> - 2.4.6-28
- Type:NA
- ID:NA
- SUG:NA
- DESC: change gcc version number on aarch64

