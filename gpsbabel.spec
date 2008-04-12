Summary:	GPSBabel - convert GPS waypoint, route and track data
Summary(pl.UTF-8):	GPSBabel - konwertowanie danych GPS: waypointów, tras i śladów
Name:		gpsbabel
Version:	1.3.4
Release:	1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/gpsbabel/%{name}-%{version}.tar.gz
# Source0-md5:	edb2a92d7d02ef1c197ce870608fc270
URL:		http://www.gpsbabel.org/
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

%build
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
%doc AUTHORS README* gpsbabel.html
%attr(755,root,root) %{_bindir}/gpsbabel
