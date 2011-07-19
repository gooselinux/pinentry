
%if 0%{?fedora} > 8 || 0%{?rhel} > 5
%define _enable_pinentry_qt4 --enable-pinentry-qt4
%define _enable_pinentry_qt --enable-pinentry-qt
%define qt3 qt3
%else
%define qt3 qt
%define _enable_pinentry_qt --enable-pinentry-qt 
%endif

Name:    pinentry
Version: 0.7.6
Release: 5%{?dist}
Summary: Collection of simple PIN or passphrase entry dialogs

Group:   Applications/System
License: GPLv2+
URL:     http://www.gnupg.org/aegypten/
Source0: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.gz.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# borrowed from opensuse
Source10: pinentry-wrapper

## Upstreamable patches
# from gpa-devel list, archives seem 404'd atm
Patch50: 0001-Fix-pinentry-gtk-2-SIGSEGV-when-unfocusing-with-g-ar.patch

BuildRequires: gtk2-devel
BuildRequires: libcap-devel
BuildRequires: ncurses-devel
%if 0%{?_enable_pinentry_qt:1}
BuildRequires: %{qt3}-devel
%endif
%if 0%{?_enable_pinentry_qt4:1}
BuildRequires: qt4-devel
%endif

Requires(pre): %{_sbindir}/update-alternatives
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

Provides: %{name}-curses = %{version}-%{release}

%description
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the curses (text) based version of the PIN entry dialog.

%package gtk
Summary: Passphrase/PIN entry dialog based on GTK+
Group:   Applications/System
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
%description gtk
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the GTK GUI based version of the PIN entry dialog.

%package qt
Summary: Passphrase/PIN entry dialog based on Qt3
Group:   Applications/System
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
%description qt
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the Qt3 GUI based version of the PIN entry dialog.

%package qt4
Summary: Passphrase/PIN entry dialog based on Qt4
Group:   Applications/System
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
%description qt4
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the Qt4 GUI based version of the PIN entry dialog.
Support for Qt4 is new, and a bit experimental.


%prep
%setup -q

%patch50 -p1 -b .rhbug_520236

# hack around auto* madness, lack of proper support for moc
%if %{?_enable_pinentry_qt4:1}
pushd qt4
moc-qt4 pinentrydialog.h > pinentrydialog.moc
moc-qt4 qsecurelineedit.h > qsecurelineedit.moc
popd
%endif

%build
%if 0%{?_enable_pinentry_qt:1}
unset QTDIR || : ; . /etc/profile.d/qt.sh
%endif

%configure \
  --disable-rpath \
  --disable-dependency-tracking \
  --disable-pinentry-gtk \
  %{?_enable_pinentry_qt} %{!?_enable_pinentry_qt:--disable-pinentry-qt} \
  %{?_enable_pinentry_qt4} %{!?_enable_pinentry_qt4:--disable-pinentry-qt4} 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Backwards compatibility
ln -s pinentry-gtk-2 $RPM_BUILD_ROOT%{_bindir}/pinentry-gtk

install -p -m755 -D %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/pinentry

# unpackaged files
rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT


# alternatives dropped at 0.7.6-3 (use %%trigger instead?)
%pre
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-curses ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-gtk ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt ||:

%post
if [ -f %{_infodir}/pinentry.info* ]; then
/sbin/install-info %{_infodir}/pinentry.info %{_infodir}/dir ||:
fi

%preun
if [ $1 -eq 0 -a -f %{_infodir}/pinentry.info* ] ; then
  /sbin/install-info --delete %{_infodir}/pinentry.info %{_infodir}/dir ||:
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO
%{_bindir}/pinentry-curses
%{_bindir}/pinentry
%{_infodir}/pinentry.info*

%files gtk
%defattr(-,root,root,-)
%{_bindir}/pinentry-gtk
%{_bindir}/pinentry-gtk-2

%files qt
%defattr(-,root,root,-)
%{_bindir}/pinentry-qt

%if 0%{?_enable_pinentry_qt4:1}
%files qt4
%defattr(-,root,root,-)
%{_bindir}/pinentry-qt4
%endif


%changelog
* Sun Apr 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-5
- pinentry-gtk -g segfaults on focus change (#520236)

* Wed Sep 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-4
- Errors installing with --excludedocs (#515925)

* Wed Sep 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-3
- drop alternatives, use app-wrapper instead (borrowed from opensuse)
- -qt4 experimental subpkg, -qt includes qt3 version again  (#523488)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-1
- pinentry-0.7.6
- -qt switched qt4 version, where applicable (f9+, rhel6+)
- fixup scriptlets

* Sat Apr 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.5-1
- pinentry-0.7.5

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.7.4-5
- pinentry failed massrebuild attempt for GCC 4.3 (#434400)

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.7.4-4
- s/qt-devel/qt3-devel/ (f9+)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.4-3
- Autorebuild for GCC 4.3

* Sun Feb 17 2008 Adam Tkac <atkac redhat com> - 0.7.4-2
- rebuild against new libcap

* Sun Dec 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.4-1
- pinentry-0.7.4
- BR: libcap-devel

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.3-2
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.3-1
- pinentry-0.7.3
- License: GPLv2+

* Thu May 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.2-15
- respin (for ppc64)

* Mon Dec 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-14
- -14 respin (to help retire ATrpms pinentry pkg)

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-3
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-2
- fc6 respin

* Wed Mar 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 
- fc5: gcc/glibc respin

* Tue Oct 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.2-1
- 0.7.2, docs patch applied upstream.
- Switch to GTK2 in -gtk.
- Fine tune dependencies.
- Build with dependency tracking disabled.
- Clean up obsolete pre-FC2 support.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.7.1-4
- rebuilt

* Wed Jun 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.3
- BuildRequires qt-devel >= 3.2.

* Sat May 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.2
- Spec cleanups.

* Sat Apr 24 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.1
- Update to 0.7.1.

* Fri Dec 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.0-0.fdr.1
- Update to 0.7.0.
- Split GTK+ and QT dialogs into subpackages.

* Thu Jul 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.9-0.fdr.1
- Update to 0.6.9.
- Smoother experience with --excludedocs.
- Don't change alternative priorities on upgrade.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.8-0.fdr.1
- Update to current Fedora guidelines.

* Tue Feb 12 2003 Warren Togami <warren@togami.com> 0.6.8-1.fedora.3
- info/dir temporary workaround

* Sat Feb  8 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.6.8-1.fedora.1
- First Fedora release.
