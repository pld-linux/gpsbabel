#
# Conditional build:
%bcond_without	doc		# HTML documentation
%bcond_without	qt5		# Qt5 instead of Qt6
%bcond_without	qtwebengine	# map preview using Qt WebEngine
#
%define		qt5_ver	5.12
%define		qt6_ver	6.0
%define         fver	%(echo %{version} | tr . _)

# Qt WebEngine has limited availability
%if %{with qt5}
%ifnarch %{ix86} %{x8664} %{arm} aarch64
%undefine with_qtwebengine
%endif
%else
%ifnarch %{x8664} aarch64
%undefine with_qtwebengine
%endif
%endif

Summary:	GPSBabel - convert GPS waypoint, route and track data
Summary(pl.UTF-8):	GPSBabel - konwertowanie danych GPS: waypointów, tras i śladów
Name:		gpsbabel
Version:	1.9.0
Release:	1
License:	GPL v2+
Group:		Applications/Engineering
# Source0Download via POST form at https://www.gpsbabel.org/download.html#downloading
# version=1.5.4
# token=$(curl -s http://www.gpsbabel.org/download.html | sed -rne 's/.*gpsbabel-'$version'\.tar\.gz.*token.*value="([^"]+)".*/\1/p' | head -n1)
# curl -F "token=$token" -F "dl=gpsbabel-$version.tar.gz" http://www.gpsbabel.org/plan9.php -o gpsbabel-$version.tar.gz
#Source0Download: https://github.com/GPSBabel/gpsbabel/tags
Source0:	https://github.com/GPSBabel/gpsbabel/archive/%{name}_%{fver}.tar.gz
# Source0-md5:	8555b7b4c89fbae832451ed0679e04f0
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-no-jing.patch
Patch2:		gmapbase.patch
Patch4:		privacy.patch
URL:		http://www.gpsbabel.org/
BuildRequires:	cmake >= 3.11
BuildRequires:	desktop-file-utils
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shapelib-devel
BuildRequires:	zlib-devel >= 1.2.9
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= %{qt5_ver}
%else
BuildRequires:	Qt6Core-devel >= %{qt6_ver}
%endif
%if %{with qt5}
BuildRequires:	Qt5Gui-devel >= %{qt5_ver}
BuildRequires:	Qt5Network-devel >= %{qt5_ver}
BuildRequires:	Qt5SerialPort-devel >= %{qt5_ver}
%if %{with qtwebengine}
BuildRequires:	Qt5WebChannel-devel >= %{qt5_ver}
BuildRequires:	Qt5WebEngine-devel >= %{qt5_ver}
%endif
BuildRequires:	Qt5Widgets-devel >= %{qt5_ver}
BuildRequires:	Qt5Xml-devel >= %{qt5_ver}
BuildRequires:	qt5-build >= %{qt5_ver}
BuildRequires:	qt5-linguist >= %{qt5_ver}
BuildRequires:	qt5-qmake >= %{qt5_ver}
%else
BuildRequires:	Qt6Gui-devel >= %{qt6_ver}
BuildRequires:	Qt6Network-devel >= %{qt6_ver}
BuildRequires:	Qt6Qt5Compat-devel >= %{qt6_ver}
BuildRequires:	Qt6SerialPort-devel >= %{qt6_ver}
%if %{with qtwebengine}
BuildRequires:	Qt6WebChannel-devel >= %{qt6_ver}
BuildRequires:	Qt6WebEngine-devel >= %{qt6_ver}
%endif
BuildRequires:	Qt6Widgets-devel >= %{qt6_ver}
BuildRequires:	Qt6Xml-devel >= %{qt6_ver}
BuildRequires:	qt6-build >= %{qt6_ver}
BuildRequires:	qt6-linguist >= %{qt6_ver}
%endif
%if %{with doc}
BuildRequires:	docbook-dtd50-xml
BuildRequires:	docbook-style-xsl-ns
BuildRequires:	libxslt-progs
# xmllint for validation
BuildRequires:	libxml2-progs
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with qt5}
%define		translationdir	%{_datadir}/qt5/translations
%else
%define		translationdir	%{_datadir}/qt6/translations
%endif

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
%patch -P0 -p1
%patch -P2 -p1
%patch -P4 -p1

%if %{with qt5}
%{__sed} -i -e '/QT NAMES / s/Qt6 //' gui/CMakeLists.txt
%endif

%build
install -d build
cd build
%cmake .. \
	%{!?with_qtwebengine:-DGPSBABEL_MAPPREVIEW=OFF} \
	-DGPSBABEL_WITH_SHAPELIB=pkgconfig \
	-DGPSBABEL_WITH_ZLIB=findpackage

%{__make}

%{__make} package_app
cd ..

%if %{with doc}
# docs generation requires in-source build
%cmake . \
	%{!?with_qtwebengine:-DGPSBABEL_MAPPREVIEW=OFF}

%{__make} gpsbabel.html
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{translationdir}}

install build/gui/GPSBabelFE/gpsbabel $RPM_BUILD_ROOT%{_bindir}
install build/gui/GPSBabelFE/gpsbabelfe $RPM_BUILD_ROOT%{_bindir}
cp -p build/gui/GPSBabelFE/gmapbase.html $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p build/gui/GPSBabelFE/translations/gpsbabel*.qm $RPM_BUILD_ROOT%{translationdir}

desktop-file-install \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	%{SOURCE1}

install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.igc README.md SECURITY.md %{?with_doc:gpsbabel.html}
%attr(755,root,root) %{_bindir}/gpsbabel
%lang(de) %{translationdir}/gpsbabel_de.qm
%lang(es) %{translationdir}/gpsbabel_es.qm
%lang(fr) %{translationdir}/gpsbabel_fr.qm
%lang(hu) %{translationdir}/gpsbabel_hu.qm
%lang(it) %{translationdir}/gpsbabel_it.qm
%lang(ru) %{translationdir}/gpsbabel_ru.qm

%files gui
%defattr(644,root,root,755)
%doc gui/{README.gui,TODO}
%attr(755,root,root) %{_bindir}/gpsbabelfe
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/gmapbase.html
%lang(de) %{translationdir}/gpsbabelfe_de.qm
%lang(es) %{translationdir}/gpsbabelfe_es.qm
%lang(fr) %{translationdir}/gpsbabelfe_fr.qm
%lang(hu) %{translationdir}/gpsbabelfe_hu.qm
%lang(it) %{translationdir}/gpsbabelfe_it.qm
%lang(ru) %{translationdir}/gpsbabelfe_ru.qm
%{_desktopdir}/gpsbabel.desktop
%{_iconsdir}/hicolor/*/apps/gpsbabel.png
