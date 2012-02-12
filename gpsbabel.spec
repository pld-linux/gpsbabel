# TODO
# - fix as-needed fix needed
#
# Conditional build:
%bcond_without	qt4		# build Qt4 GUI

%define		qtver		4.7.1
Summary:	GPSBabel - convert GPS waypoint, route and track data
Summary(pl.UTF-8):	GPSBabel - konwertowanie danych GPS: waypointów, tras i śladów
Name:		gpsbabel
Version:	1.4.3
Release:	1
License:	GPL
Group:		Applications
# Source0Download via POST form at https://www.gpsbabel.org/download.html#downloading
# token=$(curl -s http://www.gpsbabel.org/download.html | sed -rne 's/.*token.*value="([^"]+)".*/\1/p' | head -n1)
# version=1.4.3
# curl -F "token=$token" -F "dl=gpsbabel-$version.tar.gz" http://www.gpsbabel.org/plan9.php -o gpsbabel-$version.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	916f7e124f6df911a24e1ea323e9c529
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-auto.patch
Patch1:		use-system-shapelib.patch
URL:		http://www.gpsbabel.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	libusb-devel
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	shapelib-devel
%if %{with qt4}
BuildRequires:	QtCore-devel >= %{qtver}
BuildRequires:	QtGui-devel >= %{qtver}
BuildRequires:	QtNetwork-devel >= %{qtver}
BuildRequires:	QtWebKit-devel >= %{qtver}
BuildRequires:	QtXml-devel >= %{qtver}
BuildRequires:	desktop-file-utils
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-linguist >= %{qtver}
BuildRequires:	qt4-qmake >= %{qtver}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# FIXME
%define		filterout_ld	-Wl,--as-needed

%define		translationdir	%{_datadir}/qt4/translations

%description
Converts GPS waypoint, route and track data from one format type to
another.

%description -l pl.UTF-8
GPSBabel konwertuje dane GPS: waypointy, trasy i ślady z jednego
formatu na drugi.

%package gui
Summary:	Qt GUI interface for GPSBabel
License:	GPL v2+
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description gui
Qt GUI interface for GPSBabel

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Use system shapelib instead of bundled partial shapelib
mv shapelib{,.bundled}

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-zlib=system \
	--with-doc=./manual
%{__make}

%{__perl} xmldoc/makedoc
%{__make} gpsbabel.html

%if %{with qt4}
cd gui
qmake-qt4
lrelease-qt4 *.ts
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with qt4}
%{__make} -C gui install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{translationdir}}
install -p gui/objects/gpsbabelfe-bin $RPM_BUILD_ROOT%{_bindir}
install -p gui/gpsbabel*_*.qm         $RPM_BUILD_ROOT%{translationdir}

desktop-file-install \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	%{SOURCE1}

install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

#%find_lang %{name} --with-qt --all-name
# TODO: patch find lang
cat <<EOF > %{name}.lang
%lang(de) %{translationdir}/gpsbabel_de.qm
%lang(es) %{translationdir}/gpsbabel_es.qm
%lang(fr) %{translationdir}/gpsbabel_fr.qm
%lang(hu) %{translationdir}/gpsbabel_hu.qm
%lang(it) %{translationdir}/gpsbabel_it.qm
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
%doc AUTHORS README*
#%doc gpsbabel.html
%attr(755,root,root) %{_bindir}/gpsbabel

%if %{with qt4}
%files gui -f %{name}.lang
%defattr(644,root,root,755)
%doc gui/{AUTHORS,README*,TODO}
%attr(755,root,root) %{_bindir}/gpsbabelfe-bin
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
# XXX move to qt.spec?
%dir %{translationdir}
%endif
