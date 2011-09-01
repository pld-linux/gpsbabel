# TODO
# - Qt gui
# - Use system shapelib instead of bundled partial shapelib
Summary:	GPSBabel - convert GPS waypoint, route and track data
Summary(pl.UTF-8):	GPSBabel - konwertowanie danych GPS: waypointów, tras i śladów
Name:		gpsbabel
Version:	1.4.2
Release:	1
License:	GPL
Group:		Applications
# Source0Download via POST form at https://www.gpsbabel.org/download.html#downloading
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/gpsbabel/%{name}-%{version}.tar.gz/76ea9f7852be2e98aa18976c4697ca93/%{name}-%{version}.tar.gz
# Source0-md5:	76ea9f7852be2e98aa18976c4697ca93
Patch0:		%{name}-auto.patch
URL:		http://www.gpsbabel.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	libusb-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Converts GPS waypoint, route and track data from one format type to
another.

%description -l pl.UTF-8
GPSBabel konwertuje dane GPS: waypointy, trasy i ślady z jednego
formatu na drugi.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README*
#%doc gpsbabel.html
%attr(755,root,root) %{_bindir}/gpsbabel
