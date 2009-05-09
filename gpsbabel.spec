Summary:	GPSBabel - convert GPS waypoint, route and track data
Summary(pl.UTF-8):	GPSBabel - konwertowanie danych GPS: waypointów, tras i śladów
Name:		gpsbabel
Version:	1.3.6
Release:	2
License:	GPL
Group:		Applications
# Source0:	http://www.gpsbabel.org/plan9.php?dl=%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	1571b31f8f06f722995449dbff01ca49
Patch0:		%{name}-auto.patch
URL:		http://www.gpsbabel.org/
BuildRequires:	automake
BuildRequires:	autoconf
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
%patch0 -p0

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
%doc AUTHORS README* gpsbabel.html
%attr(755,root,root) %{_bindir}/gpsbabel
