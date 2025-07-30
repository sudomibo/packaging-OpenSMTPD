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
%service_add_post %{name}.service

%preun
%service_del_preun %{name}.service

%postun
%service_del_postun %{name}.service

%files
%{_sysusersdir}/%{name}-user.conf
%attr(0555,root,root) %{_bindir}/smtp
%config(noreplace) %{_sysconfdir}/smtpd.conf
%dir %{_sysconfdir}/mail
%config(noreplace) %{_sysconfdir}/mail/aliases
%{_unitdir}/%{name}.service
%{_sbindir}/rc%{name}
%dir %{_libexecdir}/opensmtpd
%attr(0555,root,root) %{_libexecdir}/opensmtpd/encrypt
%attr(4555,root,root) %{_libexecdir}/opensmtpd/lockspool
%attr(0555,root,root) %{_libexecdir}/opensmtpd/mail.lmtp
%attr(0555,root,root) %{_libexecdir}/opensmtpd/mail.local
%attr(0555,root,root) %{_libexecdir}/opensmtpd/mail.maildir
%attr(0555,root,root) %{_libexecdir}/opensmtpd/mail.mboxfile
%attr(0555,root,root) %{_libexecdir}/opensmtpd/mail.mda
%attr(2555,root, _smtpq) %{_sbindir}/smtpctl
%attr(0555,root,root) %{_sbindir}/smtpd
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

