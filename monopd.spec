Summary:	A dedicated game server daemon for playing Monopoly-like board games
Summary(pl):	Dedykowany serwer dla gier planszowych typu Monopoly
Name:		monopd
Version:	0.7.0
Release:	1
License:	LGPL/GPL
Group:		Libraries
Source0:	http://easynews.dl.sourceforge.net/sourceforge/monopd/%{name}-%{version}.tar.bz2
# Source0-md5:	8f2b76309f979bc7245d1034651ae724
Source1:	%{name}.init
Patch0:		%{name}-DESTDIR.patch
URL:		http://unixcode.org/monopd/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libcapsinetwork-devel >= 0.2.2
BuildRequires:	libmath++ >= 0.0.3
BuildRequires:	libstdc++-devel
Requires(post,preun):   /sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Monopd is a dedicated game server daemon for playing Monopoly-like
board games. Clients such as Atlantik connect to the server and
communicate using short commands and XML messages.

%description -l pl
Monopd to dedykowany serwer dla gier planszowych typu Monopoly.
Klienci tacy jak Atlantik ³±cz± siê z serwerem i komunikuj± przy
u¿yciu krótkich komend i komunikatów XML.

%prep
%setup -q
%patch0 -p1

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/monopd.conf{-dist,}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/monopd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add monopd
if [ -f /var/lock/subsys/monopd ]; then
	/etc/rc.d/init.d/monopd restart >&2
else    
	echo "Run \"/etc/rc.d/init.d/monopd start\" to start monopd." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/monopd ]; then
		/etc/rc.d/init.d/monopd stop
	fi
	/sbin/chkconfig --del monopd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO README.monopigator doc/api/gameboard
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/monopd.conf
%attr(754,root,root) /etc/rc.d/init.d/monopd
%dir %{_datadir}/monopd
%dir %{_datadir}/monopd/games
%{_datadir}/monopd/games/*
