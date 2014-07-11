%define	major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	An open-source audio processing library
Name:		soundtouch
Version:	1.7.1
Release:	7
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.surina.net/soundtouch/
Source0:	http://www.surina.net/soundtouch/%{name}-%{version}.tar.gz
Patch0:		soundtouch-automake-1.13.patch
BuildRequires:	dos2unix
Conflicts:	SoundTouch

%track
prog %name = {
	url = http://www.surina.net/soundtouch/sourcecode.html
	regex = "library v(__VER__) source code release"
	version = %version
}

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
%setup -q -n %{name}
%apply_patches

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

# fix permissions
chmod 644 COPYING.TXT README.html

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix

sh ./bootstrap

%build

%configure2_5x \
    --enable-shared

%make

%install
rm -rf %{buildroot}

%makeinstall

# cleanup
rm -rf %{buildroot}{/usr/doc,%_libdir/*.la}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING.TXT README.html
%{_bindir}/soundstretch

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/soundtouch
%{_includedir}/soundtouch/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/soundtouch*.pc
%{_datadir}/aclocal/*


%changelog
* Wed Feb 22 2012 Götz Waschk <waschk@mandriva.org> 1.6.0-2mdv2012.0
+ Revision: 779123
- reenable sse2 to make it build
- manually remove libtool archive

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 1.6.0
    - drop patch 0
    - disable -msse2 flags on ix86

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-2
+ Revision: 670001
- mass rebuild

* Sat Feb 12 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.0-1
+ Revision: 637384
- update to new version 1.5.0

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-3mdv2011.0
+ Revision: 607551
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-2mdv2010.1
+ Revision: 521162
- rebuilt for 2010.1

  + Emmanuel Andry <eandry@mandriva.org>
    - check major

* Mon Jun 08 2009 Jérôme Brenier <incubusss@mandriva.org> 1.4.0-1mdv2010.0
+ Revision: 384101
- update to new version 1.4.0
- drop gcc43 and linkage patches (no more needed)
- add a patch to fix build on x86_64 (from fedora, rediffed)
- fix license

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.3.1-5mdv2009.0
+ Revision: 265739
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri May 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-4mdv2009.0
+ Revision: 210368
- fix build
- added a gcc43 patch from fedora

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-3mdv2008.1
+ Revision: 179515
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-2mdv2008.0
+ Revision: 58523
- bump release
- drop P0, it will be fixed elsewhere

* Wed Aug 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-1mdv2008.0
+ Revision: 57606
- Import soundtouch



* Wed Aug 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-1mdv2008.0
- renamed from SoundTouch to soundtouch and obey current specs

* Wed Aug 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-2mdv2007.0
- 1.3.1 (not rc4)

* Thu Jun 22 2006 Erwan Velu <erwan@seanodes.com> 1.3.1-1
- 1.3.1

* Sun Mar 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-0.rc4.1mdk
- 1.3.1rc4
- rediffed the asterisk patch (now P0)

* Fri Mar 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-0.rc3.1mdk
- 1.3.1rc3
- added P1 so that we can integrate voicechanger into asterisk
- enable shared libs

* Fri Jul 15 2005 Stew Benedict <sbenedict@mandriva.com> 1.3.0-1mdk
- 1.3.0, update p0

* Fri Nov 12 2004 Erwan Velu <erwan@seanodes.com> 1.2.1-1mdk
- Frist Release 
