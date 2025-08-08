#
# spec file for package OpenSMTPD
#
# Copyright (c) 2025 SUSE LLC and contributors
# Copyright (c) 2025 SUSE Software Solutions
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           OpenSMTPD
%global         name_lowercase %(echo -n "%{name}" | tr '[:upper:]' '[:lower:]')
Version:        7.7.0p0
Release:        0
Summary:        A free implementation of the server-side SMTP protocol
License:        BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause AND ISC
URL:            https://www.opensmtpd.org/
Group:          Productivity/Networking/Email/Servers
Source:         https://github.com/OpenSMTPD/OpenSMTPD/releases/download/%{version}/opensmtpd-%{version}.tar.gz
Source1:        %{name}-user.conf
Source2:        %{name}.service
BuildRequires:  systemd-rpm-macros
BuildRequires:  sysuser-tools
%sysusers_requires
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  libtool
BuildRequires:  netcfg
BuildRequires:  sed
BuildRequires:  pkgconfig(libevent)
BuildRequires:  pkgconfig(libopenssl)
BuildRequires:  pkgconfig(zlib)
Provides:       smtp_daemon
Conflicts:      busybox-sendmail
Conflicts:      exim
Conflicts:      msmtp-mta
Conflicts:      postfix
Conflicts:      postfix-bdb
Conflicts:      sendmail

%description
OpenSMTPD is a FREE implementation of the server-side SMTP protocol as defined by RFC 5321, with some additional standard extensions.

It allows ordinary machines to exchange e-mails with other systems speaking the SMTP protocol.

%prep
%setup -q -n %{name_lowercase}-%{version}
./bootstrap

%build
%sysusers_generate_pre %{SOURCE1} %{name} %{name}-user.conf
sed -i "s;@rundir@;%{_rundir};g" %{SOURCE2}
%configure --with-path-empty=%{_sharedstatedir}/empty --with-path-pidfile=%{_rundir}
%make_build

%install
install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}-user.conf
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
mkdir -p %{buildroot}%{_sysconfdir}/mail
ln -s %{_sysconfdir}/aliases %{buildroot}%{_sysconfdir}/mail/aliases
%make_install

%check
make check

%pre -f %{name}.pre
%service_add_pre %{name}.service

%post
%service_add_post %{name}.service

%preun
%service_del_preun %{name}.service

%postun
%service_del_postun %{name}.service

%files
%{_sysusersdir}/%{name}-user.conf
%config(noreplace) %{_sysconfdir}/smtpd.conf
%dir %{_sysconfdir}/mail
%config(noreplace) %{_sysconfdir}/mail/aliases
%{_unitdir}/%{name}.service
%{_bindir}/smtp
%dir %{_libexecdir}/%{name_lowercase}
%{_libexecdir}/%{name_lowercase}/encrypt
%{_libexecdir}/%{name_lowercase}/lockspool
%{_libexecdir}/%{name_lowercase}/mail.lmtp
%{_libexecdir}/%{name_lowercase}/mail.local
%{_libexecdir}/%{name_lowercase}/mail.maildir
%{_libexecdir}/%{name_lowercase}/mail.mboxfile
%{_libexecdir}/%{name_lowercase}/mail.mda
%attr(-,-,_smtpq) %{_sbindir}/smtpctl
%{_sbindir}/smtpd
%{_mandir}/man1/lockspool.1*
%{_mandir}/man1/smtp.1*
%{_mandir}/man5/aliases.5*
%{_mandir}/man5/forward.5*
%{_mandir}/man5/smtpd.conf.5*
%{_mandir}/man5/table.5*
%{_mandir}/man7/smtpd-filters.7*
%{_mandir}/man7/smtpd-tables.7*
%{_mandir}/man8/mail.lmtp.8*
%{_mandir}/man8/mail.local.8*
%{_mandir}/man8/mail.maildir.8*
%{_mandir}/man8/mail.mboxfile.8*
%{_mandir}/man8/mail.mda.8*
%{_mandir}/man8/makemap.8*
%{_mandir}/man8/newaliases.8*
%{_mandir}/man8/sendmail.8*
%{_mandir}/man8/smtpctl.8*
%{_mandir}/man8/smtpd.8*
%license LICENSE

%changelog
