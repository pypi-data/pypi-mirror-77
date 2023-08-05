Name: libvslvm
Version: 20200817
Release: 1
Summary: Library to access the Linux Logical Volume Manager (LVM) volume system
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libvslvm
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
             
BuildRequires: gcc             

%description -n libvslvm
Library to access the Linux Logical Volume Manager (LVM) volume system

%package -n libvslvm-static
Summary: Library to access the Linux Logical Volume Manager (LVM) volume system
Group: Development/Libraries
Requires: libvslvm = %{version}-%{release}

%description -n libvslvm-static
Static library version of libvslvm.

%package -n libvslvm-devel
Summary: Header files and libraries for developing applications for libvslvm
Group: Development/Libraries
Requires: libvslvm = %{version}-%{release}

%description -n libvslvm-devel
Header files and libraries for developing applications for libvslvm.

%package -n libvslvm-python2
Obsoletes: libvslvm-python < %{version}
Provides: libvslvm-python = %{version}
Summary: Python 2 bindings for libvslvm
Group: System Environment/Libraries
Requires: libvslvm = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libvslvm-python2
Python 2 bindings for libvslvm

%package -n libvslvm-python3
Summary: Python 3 bindings for libvslvm
Group: System Environment/Libraries
Requires: libvslvm = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libvslvm-python3
Python 3 bindings for libvslvm

%package -n libvslvm-tools
Summary: Several tools for Several tools for reading Linux Logical Volume Manager (LVM) volume systems
Group: Applications/System
Requires: libvslvm = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libvslvm-tools
Several tools for Several tools for reading Linux Logical Volume Manager (LVM) volume systems

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libvslvm
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libvslvm-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libvslvm-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvslvm.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libvslvm-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libvslvm-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libvslvm-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Aug 17 2020 Joachim Metz <joachim.metz@gmail.com> 20200817-1
- Auto-generated

