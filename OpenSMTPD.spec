#
# spec file for package OpenSMTPD
#
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


Name:           OpenSMTPD
Version:        7.7.0p0
Release:        0
Summary:        A free implementation of the server-side SMTP protocol
License:        ISC and BSD-4-Clause and BSD-3-Clause and BSD-2-Clause
URL:            https://www.opensmtpd.org/
Group:          Productivity/Networking/Email/Servers
Source:         %{name}-%{version}b0.tar.gz
Source1:        %{name}-user.conf
Source2:        %{name}.service
Source3:        %{name}.permissions
BuildRequires:  systemd-rpm-macros
BuildRequires:  sysuser-tools
%sysusers_requires
BuildRequires:  sed
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  libtool
BuildRequires:  libevent-devel
%if 0%{?suse_version} > 1600
# openSUSE Tumbleweed
BuildRequires:  libressl-devel
%else
BuildRequires:  libopenssl-devel
%endif
BuildRequires:  zlib-devel
Requires(pre):  permissions

%description
OpenSMTPD is a FREE implementation of the server-side SMTP protocol as defined by RFC 5321, with some additional standard extensions.

It allows ordinary machines to exchange e-mails with other systems speaking the SMTP protocol.

%pre -f %{name}.pre
%service_add_pre %{name}.service

%prep
%setup -q -n %{name}-%{version}b0
./bootstrap

%build
%sysusers_generate_pre %{SOURCE1} %{name} %{name}-user.conf
sed -i "s:_libexecdir:%{_libexecdir}:g" %{SOURCE3}
sed -i "s:_rundir:%{_rundir}:g" %{SOURCE2}
%configure --with-path-empty=%{_sharedstatedir}/empty --with-path-pidfile=%{_rundir}
make
strip -s mk/smtp/smtp
strip -s contrib/libexec/encrypt/encrypt
strip -s contrib/libexec/lockspool/lockspool
strip -s mk/mail/mail.lmtp/mail.lmtp
strip -s contrib/libexec/mail.local/mail.local
strip -s mk/mail/mail.maildir/mail.maildir
strip -s mk/mail/mail.mboxfile/mail.mboxfile
strip -s mk/mail/mail.mda/mail.mda
strip -s mk/smtpctl/smtpctl
strip -s mk/smtpd/smtpd

%install
install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}-user.conf
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
mkdir -p %{buildroot}%{_sysconfdir}/permissions.d
install -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/permissions.d/%{name}
# <rpmlint fix for "suse-missing-rclink">
mkdir -p %{buildroot}%{_sbindir}
pushd %{buildroot}%{_sbindir}
ln -s service rc%{name}
popd
# </rpmlint>
mkdir -p %{buildroot}%{_sysconfdir}/mail
install -D -m 0644 etc/aliases %{buildroot}%{_sysconfdir}/mail/aliases
make DESTDIR=%{buildroot} install

%check
make check

%post
%set_permissions %{_bindir}/smtp
%set_permissions %{_libexecdir}/opensmtpd/encrypt
%set_permissions %{_libexecdir}/opensmtpd/lockspool
%set_permissions %{_libexecdir}/opensmtpd/mail.lmtp
%set_permissions %{_libexecdir}/opensmtpd/mail.local
%set_permissions %{_libexecdir}/opensmtpd/mail.maildir
%set_permissions %{_libexecdir}/opensmtpd/mail.mboxfile
%set_permissions %{_libexecdir}/opensmtpd/mail.mda
%set_permissions %{_sbindir}/smtpctl
%set_permissions %{_sbindir}/smtpd
%service_add_post %{name}.service

%preun
%service_del_preun %{name}.service

%postun
%service_del_postun %{name}.service

%verifyscript
%verify_permissions -e %{_bindir}/smtp
%verify_permissions -e %{_libexecdir}/opensmtpd/encrypt
%verify_permissions -e %{_libexecdir}/opensmtpd/lockspool
%verify_permissions -e %{_libexecdir}/opensmtpd/mail.lmtp
%verify_permissions -e %{_libexecdir}/opensmtpd/mail.local
%verify_permissions -e %{_libexecdir}/opensmtpd/mail.maildir
%verify_permissions -e %{_libexecdir}/opensmtpd/mail.mboxfile
%verify_permissions -e %{_libexecdir}/opensmtpd/mail.mda
%verify_permissions -e %{_sbindir}/smtpctl
%verify_permissions -e %{_sbindir}/smtpd

%files
%{_sysusersdir}/%{name}-user.conf
%verify(not mode) %attr(0755,root,root) %{_bindir}/smtp
%config(noreplace) %{_sysconfdir}/smtpd.conf
%dir %{_sysconfdir}/mail
%config(noreplace) %{_sysconfdir}/mail/aliases
%config %{_sysconfdir}/permissions.d/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/rc%{name}
%dir %{_libexecdir}/opensmtpd
%verify(not mode) %attr(0755,root,root) %{_libexecdir}/opensmtpd/encrypt
%verify(not mode caps) %attr(4755,root,root) %{_libexecdir}/opensmtpd/lockspool
%verify(not mode) %attr(0755,root,root) %{_libexecdir}/opensmtpd/mail.lmtp
%verify(not mode) %attr(0755,root,root) %{_libexecdir}/opensmtpd/mail.local
%verify(not mode) %attr(0755,root,root) %{_libexecdir}/opensmtpd/mail.maildir
%verify(not mode) %attr(0755,root,root) %{_libexecdir}/opensmtpd/mail.mboxfile
%verify(not mode) %attr(0755,root,root) %{_libexecdir}/opensmtpd/mail.mda
%verify(not mode caps) %attr(4755,root, _smtpq) %{_sbindir}/smtpctl
%verify(not mode) %attr(0755,root,root) %{_sbindir}/smtpd
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

