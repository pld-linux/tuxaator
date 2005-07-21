%include	/usr/lib/rpm/macros.perl
Summary:	A lightweight IRC bot/dictionary, easy to set up, easy to localize
Summary(pl):	Lekki bot/s³ownik IRC, ³atwy do postawienia, ³atwy do zlokalizowania
Name:		tuxaator
Version:	2.0
%define	_pre	pre2
%define	_snap	20050718
Release:	0.%{_pre}.%{_snap}.21
Epoch:		0
License:	BSD
Group:		Applications/Communications
Source0:	http://glen.alkohol.ee/pld/tuxaator/%{name}-%{_snap}.tar.bz2
# Source0-md5:	3451a4d019dbf364d5983541b9fc8fb5
Source1:	%{name}.init
Patch0:		%{name}-schema.patch
Patch1:		%{name}-basedir.patch
URL:		http://tuxaator.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(pre):  /usr/bin/getgid
Requires(pre):  /usr/sbin/groupadd
Requires(postun):	/usr/sbin/groupdel
Provides:	group(tuxaator)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_appdir %{_datadir}/%{name}

%description
A lightweight IRC bot/dictionary, easy to set up, easy to localize.

%description -l pl
Lekki bot/s³ownik IRC, ³atwy do postawienia, ³atwy do zlokalizowania.

%package init
Summary:	tuxaator initscript
Summary(pl):	Skrypt init dla tuxaatora
Group:		Applications/Communications
PreReq:		rc-scripts >= 0.4.0.17
PreReq:		%{name} = %{epoch}:%{version}-%{release}
Requires(post,preun):	/sbin/chkconfig
Requires(pre):  /bin/id
Requires(pre):  /usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Provides:	user(tuxaator)

%description init
Initscript for tuxaator IRC bot.

%description init -l pl
Skrypt init dla bota IRC-owego tuxaator.

%prep
%setup -q -n %{name}-%{_snap}
%patch0 -p1
%patch1 -p1
find -name CVS -print0 | xargs -0 rm -rf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir},%{_bindir},%{perl_vendorlib},/etc/rc.d/init.d}

cp -a *.txt reasons $RPM_BUILD_ROOT%{_appdir}
cp -a %{name} *.pm Plugins $RPM_BUILD_ROOT%{_appdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
cd %{_appdir}
exec perl %{name} "$@"
EOF

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

for a in config/*.dist; do
	install $a $RPM_BUILD_ROOT%{_sysconfdir}/$(basename $a .dist)
done
install config/{rss.tux,messages.*} $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -P %{name}-init -g 153 %{name}

%postun
if [ "$1" = "0" ]; then
	%groupremove %{name}
fi

%pre init
%useradd -P %{name}-init -u 153 -g %{name} -c "Tuxaator" %{name}

%post init
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun init
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun init
if [ "$1" = "0" ]; then
	%userremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS Changelog HELP INSTALL LICENSE UPGRADING
%doc *.sql upgrades/ scripts/
%dir %attr(750,root,tuxaator) %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,tuxaator) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%{_appdir}

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/tuxaator
