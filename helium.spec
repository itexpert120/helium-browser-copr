%global             full_name helium
%global             application_name helium
%global             debug_package %{nil}

Name:               helium
Version:            0.4.12.1
Release:            1%{?dist}
Summary:            Helium Browser

License:            GPL-3.0
URL:                https://github.com/imputnet/helium-linux
Source0:            https://github.com/imputnet/helium-linux/releases/download/0.4.12.1/helium-0.4.12.1-x86_64_linux.tar.xz
Source1:            %{full_name}.desktop
Source2:            %{full_name}

ExclusiveArch:      x86_64

Recommends:         (plasma-browser-integration if plasma-workspace)
Recommends:         (gnome-browser-connector if gnome-shell)

Requires(post):     gtk-update-icon-cache

%description
This is a package of the Helium web browser for x86_64.
Helium Browser is a Chromium-based browser that focuses on privacy and performance.

Bugs related to Helium should be reported directly to the Helium GitHub repo:
<https://github.com/imputnet/helium/issues>

Bugs related to this package should be reported at this Git project:
<https://github.com/itexpert120/helium-browser-copr>

%prep
%setup -q -n %{application_name}

%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}{/opt/%{full_name},%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/128x128/apps,%{_datadir}/icons/hicolor/64x64/apps,%{_datadir}/icons/hicolor/48x48/apps,%{_datadir}/icons/hicolor/32x32/apps,%{_datadir}/icons/hicolor/16x16/apps}

%__cp -r * %{buildroot}/opt/%{full_name}

%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications


%__install -D -m 0755 %{Source2} -t %{buildroot}%{_bindir}

%__cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%__cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%__cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%__cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%__cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png

if [ -d /usr/share/hunspell ]; then ln -Tsf /usr/share/hunspell %{buildroot}/opt/%{full_name}/dictionaries; fi
if [ -d /usr/share/hyphen ]; then ln -Tsf /usr/share/hyphen %{buildroot}/opt/%{full_name}/hyphenation; fi

%post
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor

%files
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%{_bindir}/%{full_name}
/opt/%{full_name}

%changelog
* Thu Sep 26 2024 itexpert120 <itexpert120@example.com> - 0.4.12.1-1
- Initial package for Helium Browser
