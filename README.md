# Packaging OpenSMTPD for openSUSE

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

