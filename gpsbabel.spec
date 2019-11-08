#
# Conditional build:
%bcond_without	qt5		# build Qt5 GUI
#
%define		qtver		5.11.1
%define         fver    %(echo %{version} | tr . _)

# disable qt5 on x32 until qt5-qtwebengine builds
# (python segfaults as of 20181212)
%ifarch x32
%undefine with_qt5
%endif

Summary:	GPSBabel - convert GPS waypoint, route and track data
Summary(pl.UTF-8):	GPSBabel - konwertowanie danych GPS: waypointów, tras i śladów
Name:		gpsbabel
Version:	1.6.0
Release:	1
License:	GPL v2+
Group:		Applications/Engineering
# Source0Download via POST form at https://www.gpsbabel.org/download.html#downloading
# version=1.5.4
# token=$(curl -s http://www.gpsbabel.org/download.html | sed -rne 's/.*gpsbabel-'$version'\.tar\.gz.*token.*value="([^"]+)".*/\1/p' | head -n1)
# curl -F "token=$token" -F "dl=gpsbabel-$version.tar.gz" http://www.gpsbabel.org/plan9.php -o gpsbabel-$version.tar.gz
Source0:	https://github.com/gpsbabel/gpsbabel/archive/%{name}_%{fver}.tar.gz
# Source0-md5:	accb9f923ebe1b2d2a00c67d0e1dc430
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-auto.patch
Patch1:		use-system-shapelib.patch
Patch2:		gmapbase.patch
Patch3:		%{name}-link.patch
Patch4:		privacy.patch
Patch5:		%{name}-system-minizip.patch
URL:		http://www.gpsbabel.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	docbook-style-xsl
BuildRequires:	expat-devel >= 1.95
#BuildRequires:	libusb-compat-devel >= 0.1
BuildRequires:	libxslt-progs
BuildRequires:	minizip-devel
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	shapelib-devel
BuildRequires:	zlib-devel
BuildRequires:	Qt5Core-devel >= %{qtver}
%if %{with qt5}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5WebEngine-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	desktop-file-utils
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	qt5-qmake >= %{qtver}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		translationdir	%{_datadir}/qt5/translations

%description
Converts GPS waypoint, route and track data from one format type to
another.

%description -l pl.UTF-8
GPSBabel konwertuje dane GPS: waypointy, trasy i ślady z jednego
formatu na drugi.

%package gui
Summary:	Qt GUI interface for GPSBabel
Summary(pl.UTF-8):	Graficzny interfejs Qt do programu GPSBabel
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description gui
Qt GUI interface for GPSBabel.

%description gui -l pl.UTF-8
Graficzny interfejs Qt do programu GPSBabel.

%prep
%setup -q -n %{name}-%{name}_%{fver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Use system shapelib instead of bundled partial shapelib
mv shapelib{,.bundled}

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-zlib=system \
	--with-libminizip=system \
	--with-doc=./manual
%{__make}

%{__perl} xmldoc/makedoc
%{__make} gpsbabel.html

%if %{with qt5}
cd gui
qmake-qt5
lrelease-qt5 *.ts
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with qt5}
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{translationdir}}
install -p gui/gpsbabel*_*.qm $RPM_BUILD_ROOT%{translationdir}
cp -p gui/gmapbase.html $RPM_BUILD_ROOT%{_datadir}/%{name}

desktop-file-install \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	%{SOURCE1}

install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

#%find_lang %{name} --with-qt --all-name
# TODO: patch find lang
cat <<EOF > %{name}.lang
%lang(de) %{translationdir}/gpsbabelfe_de.qm
%lang(es) %{translationdir}/gpsbabelfe_es.qm
%lang(fr) %{translationdir}/gpsbabelfe_fr.qm
%lang(hu) %{translationdir}/gpsbabelfe_hu.qm
%lang(it) %{translationdir}/gpsbabelfe_it.qm
%lang(ru) %{translationdir}/gpsbabelfe_ru.qm
EOF

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README* gpsbabel.html
%attr(755,root,root) %{_bindir}/gpsbabel

%if %{with qt5}
%files gui -f %{name}.lang
%defattr(644,root,root,755)
%doc gui/{AUTHORS,README*,TODO}
%{_desktopdir}/gpsbabel.desktop
%{_iconsdir}/hicolor/*/apps/gpsbabel.png
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/gmapbase.html
%endif
