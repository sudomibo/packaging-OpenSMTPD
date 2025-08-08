# Packaging OpenSMTPD for openSUSE

[![build result](https://build.opensuse.org/projects/home:mbozicevic/packages/OpenSMTPD/badge.svg?type=percent)](https://build.opensuse.org/package/show/home:mbozicevic/OpenSMTPD)

This repository contains materials related to packaging OpenSMTPD for openSUSE. It is organized mostly as notes for myself, but in case you found any information here helpful, e.g. in your own efforts to package something, feel free to star the repository.

## First Steps

To control which changes from the upstream end up built, the upstream repository was forked at https://github.com/sudomibo/OpenSMTPD/. In this case, it was forked from the official OpenSMTPD Portable repository at https://github.com/OpenSMTPD/OpenSMTPD. The commit at which we start packaging was tagged, e.g. with `git tag -a 7.6.0p1b0 -m "Build 0 for 7.6.0p1 (2024-10-20)"; git push origin 7.6.0p1b0`. Then, a [home project](https://build.opensuse.org/package/show/home:mbozicevic/OpenSMTPD) (good for experimentation) was created on the openSUSE Build Service and an archive of the source downloaded with the following commands:

```bash
osc checkout home:mbozicevic
cd home\:mbozicevic/
osc mkpac OpenSMTPD
wget https://github.com/sudomibo/OpenSMTPD/archive/refs/tags/7.6.0p1b0.tar.gz -O OpenSMTPD-7.6.0p1b0.tar.gz
```

In the same directory, the `spec` file was created (see https://github.com/sudomibo/packaging-OpenSMTPD/blob/main/OpenSMTPD.spec).

```bash
osc vc
osc add *.spec *.changes *.tar.gz
osc build --local-package
osc commit
osc buildlog openSUSE_Tumbleweed x86_64
```

Above described steps assume you have installed the `osc`/OBS tooling similar to how it is described in https://github.com/sudomibo/timestamp. In case you need inspiration for `osc` configuration see https://github.com/sudomibo/dotfiles/blob/main/.config/osc/oscrc.

After the spec and related files are created, the home project is submited to the devel/feeder project to get included in openSUSE Factory by submitting the following request:
```bash
osc submitrequest -m "I would like to maintain OpenSMTPD in Factory and would like to use server:mail as the devel/feeder project." home:mbozicevic/OpenSMTPD server:mail
```
After the request is approved, check if the maintainer role is assigned by running:

```bash
osc meta pkg server:mail/OpenSMTPD
```

and if not, request it with:

```bash
osc reqms server:mail/OpenSMTPD
```

The devel project is accessible at https://build.opensuse.org/package/show/server:mail/OpenSMTPD.

## Example Configuration

The [example](https://github.com/sudomibo/packaging-OpenSMTPD/tree/main/example) directory contains a simple mail server configuration and assumes that user accounts mentioned in the `users` file exist on the server. The configuration also assumes that the server has a valid IPv6 address and associated MX DNS record.

## `_service` OBS File

Instead of forking the upstream repository, tagging and downloading the tar.gz as described in the First Steps section, there is a cleaner way that reduces the risk of mishaps. OBS supports the `download_url` and `verify_file` services that do what you would expect from their name ([example](https://github.com/sudomibo/packaging-OpenSMTPD/blob/7b4b70185c0988c008a1a434ba5f158039d774ca/_service)).

Regardless, the preferred alternative seems to be to have the `download_files` service in manual mode (activating it locally with `osc service mr download_files`), and commit the upstream source tarball to OBS. That way source remains available even if upstream site is not available.

## Post-release Checklist

1. Were all binaries built with relevant security hardening flags?
2. Were all binaries properly stripped?

## FAQ

### How to add new users and groups?

OpenSMTPD by default uses two unprivileged accounts to increase security. They are defined in [OpenSMTPD-user.conf](https://github.com/sudomibo/packaging-OpenSMTPD/blob/main/OpenSMTPD-user.conf). To avoid the `rpmlint` "non-standard-gid" warning when the package is built, the users and groups are added to `configs/openSUSE/users-groups.toml` file in the `opensuse` branch of https://github.com/rpm-software-management/rpmlint/.

### How to include SUID/SGID binaries in the package?

Create a ticket according to https://en.opensuse.org/openSUSE:Package_security_guidelines#audit_bugs ([example](https://bugzilla.opensuse.org/show_bug.cgi?id=1247781)).

## TODO

* Prepare a default configuration file for openSUSE instead of shipping the one provided from upstream
* Continue hardening effort on the systemd unit/service

## Useful Links
* https://en.opensuse.org/openSUSE:Packaging_guidelines
* https://en.opensuse.org/openSUSE:Specfile_guidelines
* https://en.opensuse.org/openSUSE:Package_source_verification
* https://en.opensuse.org/openSUSE:Packaging_Conventions_RPM_Macros
* https://en.opensuse.org/openSUSE:Package_security_guidelines
* https://en.opensuse.org/openSUSE:Security_Features
* https://en.opensuse.org/openSUSE:Build_Service_cross_distribution_howto
* https://en.opensuse.org/openSUSE:Packaging_checks
* https://news.opensuse.org/2020/11/23/news-in-opensuse-packaging/
* https://en.opensuse.org/openSUSE:How_to_contribute_to_Factory
* https://en.opensuse.org/openSUSE:Build_Service_Concept_SourceService
* https://rpm.org/docs/4.20.x/manual/macros

