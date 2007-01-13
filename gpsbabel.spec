Summary:	GPSBabel converts GPS waypoint, route and track data
Summary(pl):	GPSBabel konwertuje dane GPS - waypointy, trasy i ¶lady
Name:		gpsbabel
Version:	1.3.2
Release:	1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/gpsbabel/%{name}-%{version}.tar.gz
# Source0-md5:	5a9c442bc681035b1dfdbb32b1d3fa8b
URL:		http://www.gpsbabel.org
BuildRequires:	libusb-devel
BuildRequires:	expat-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Converts GPS waypoint, route and track data from one format type to
another.

%description -l pl
GPSBabel konwertuje dane GPS - waypointy, trasy i ¶lady z jednego 
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
	DESTDIR=$RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* COPYING AUTHORS gpsbabel.html
%attr(755,root,root) %{_bindir}/gpsbabel
