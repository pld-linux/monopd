Summary:	A dedicated game server daemon for playing Monopoly-like board games
Summary(pl.UTF-8):	Dedykowany serwer dla gier planszowych typu Monopoly
Name:		monopd
Version:	0.9.3
Release:	0.1
License:	LGPL/GPL
Group:		Libraries
Source0:	http://robertjohnkaper.com/downloads/atlantik/%{name}-%{version}.tar.bz2
# Source0-md5:	d0c4876bb24e8c961012a8ef4894fe2d
Source1:	%{name}.init
URL:		http://www.robertjohnkaper.com/software/atlantik/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libcapsinetwork-devel >= 0.2.5
BuildRequires:	libmath++ >= 0.0.3
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.176
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Monopd is a dedicated game server daemon for playing Monopoly-like
board games. Clients such as Atlantik connect to the server and
communicate using short commands and XML messages.

%description -l pl.UTF-8
Monopd to dedykowany serwer dla gier planszowych typu Monopoly.
Klienci tacy jak Atlantik łączą się z serwerem i komunikują przy
użyciu krótkich komend i komunikatów w XML-u.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
	%banner %{name} -e <<EOF
Run \"/etc/rc.d/init.d/monopd start\" to start monopd.
EOF
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/monopd.conf
%attr(754,root,root) /etc/rc.d/init.d/monopd
%dir %{_datadir}/monopd
%dir %{_datadir}/monopd/games
%{_datadir}/monopd/games/*
