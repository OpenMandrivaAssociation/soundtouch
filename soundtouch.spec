%define	major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	An open-source audio processing library
Name:		soundtouch
Version:	1.3.1
Release:	%mkrel 2
Group:		System/Libraries
License:	LGPL
URL:		http://www.surina.net/soundtouch/
Source0:	http://www.surina.net/soundtouch/%{name}-%{version}.tar.bz2
BuildRequires:	dos2unix
Conflicts:	SoundTouch

%description
SoundTouch is an open-source audio processing library. It allows changing the
sound tempo, pitch and playback rate parameters independently from each other.

%package -n	%{libname}
Summary:	An open-source audio processing library
Group:          System/Libraries
Conflicts:	%{mklibname SoundTouch 0}

%description -n	%{libname}
SoundTouch is an open-source audio processing library. It allows changing the
sound tempo, pitch and playback rate parameters independently from each other.

This package contains the shared libraries for SoundTouch.

%package -n	%{develname}
Summary:	Development package with static libs and headers
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Conflicts:	%{mklibname SoundTouch 0 -d}

%description -n	%{develname}
Static libraries and header files required for compiling SoundTouch plugins.

%prep

%setup -q -n %{name}-%{version}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

# fix permissions
chmod 644 COPYING.TXT README.html

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%build

sh ./bootstrap

%configure2_5x \
    --enable-shared

%make

%install
rm -rf %{buildroot}

%makeinstall

# cleanup
rm -rf %{buildroot}/usr/doc

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING.TXT README.html
%{_bindir}/soundstretch

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/soundtouch
%{_includedir}/soundtouch/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/soundtouch*.pc
%{_datadir}/aclocal/*
