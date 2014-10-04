Summary:	MPEG 3 audio player
Name:		mpg123
Version:	1.20.1
Release:	1
License:	LGPL, GPL (mpglib)
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/mpg123/%{name}-%{version}.tar.bz2
# Source0-md5:	1b3e8765aa608e306ede1ec507b67b23
URL:		http://www.mpg123.de/
Patch1:		%{name}-am.patch
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkg-config
BuildRequires:	pulseaudio-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mpg123 is a fast, free (for non-commercial use) and portable MPEG
audio player for Unix. It supports MPEG 1.0/2.0 layers 1, 2 and 3
(those famous "MP3" files). For full CD quality playback (44 kHz, 16
bit, stereo) a Pentium, SPARCstation10, DEC Alpha or similar CPU is
required. Mono and/or reduced quality playback (22 kHz or 11 kHz) is
even possible on i486 CPUs.

%package libs
Summary:	An optimized MPEG Audio decoder library
Group:		Libraries

%description libs
An optimized MPEG Audio decoder library.

%package libs-devel
Summary:	Header file for mpg123 library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	alsa-lib-devel
Requires:	pulseaudio-devel

%description libs-devel
Header file for mpg123 library.

%prep
%setup -q
%patch1 -p1

rm -rf libltdl

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-ltdl-install=no	\
	--with-audio=alsa,pulse		\
%ifarch %{ix86}
	--with-cpu=x86			\
%endif
%ifarch %{x8664}
	--with-cpu=x86-64		\
%endif
	--with-default-audio=alsa	\
	--with-module-suffix=.so	\
	--with-optimization=0
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/BENCHMARKING doc/BUGS ChangeLog README doc/README.remote doc/TODO doc/README.3DNOW
%attr(755,root,root) %{_bindir}/mpg123
%attr(755,root,root) %{_bindir}/mpg123-id3dump
%attr(755,root,root) %{_bindir}/mpg123-strip
%attr(755,root,root) %{_bindir}/out123

%dir %{_libdir}/mpg123
%attr(755,root,root) %{_libdir}/mpg123/output_alsa.*
%attr(755,root,root) %{_libdir}/mpg123/output_dummy.*
%attr(755,root,root) %{_libdir}/mpg123/output_pulse*
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%doc NEWS.libmpg123
%attr(755,root,root) %ghost %{_libdir}/libmpg123.so.0
%attr(755,root,root) %{_libdir}/libmpg123.so.*.*.*

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmpg123.so
%{_includedir}/mpg123.h
%{_pkgconfigdir}/libmpg123.pc

