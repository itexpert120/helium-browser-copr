%global             full_name helium
%global             application_name helium
%global             debug_package %{nil}

Name:               helium
Version:            0.4.12.1
Release:            1%{?dist}
Summary:            Private, fast, and honest web browser

License:            GPL-3.0-only
URL:                https://github.com/imputnet/helium
Source0:            https://github.com/imputnet/helium-linux/releases/download/0.4.12.1/helium-0.4.12.1-x86_64_linux.tar.xz
Source1:            %{full_name}.desktop
Source2:            %{full_name}.sh

BuildRequires:      tar
BuildRequires:      xz

ExclusiveArch:      x86_64

Recommends:         (plasma-browser-integration if plasma-workspace)
Recommends:         (gnome-browser-connector if gnome-shell)

# Runtime dependencies for Chromium-based browser
Requires:           gtk3
Requires:           nss
Requires:           alsa-lib
Requires:           xdg-utils
Requires(post):     gtk-update-icon-cache
Requires(postun):   gtk-update-icon-cache

%description
Helium is a Chromium-based web browser that focuses on privacy and performance.
It provides best privacy by default, unbiased ad-blocking, no bloat and no noise.

Features:
- Built-in ad and tracker blocking with uBlock Origin
- No telemetry or analytics
- Based on Chromium with privacy enhancements
- Zero web requests on first launch

Bugs related to Helium should be reported directly to the Helium GitHub repo:
<https://github.com/imputnet/helium/issues>

Bugs related to this package should be reported at this Git project:
<https://github.com/itexpert120/helium-browser-copr>

%prep
%setup -q -c -n %{application_name}

%install
rm -rf %{buildroot}

# Create directory structure
install -d %{buildroot}/opt/%{full_name}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps

# Install all browser files
cp -r * %{buildroot}/opt/%{full_name}/

# Install desktop file and wrapper script
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{full_name}.desktop
install -D -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/%{full_name}

# Install icons at different sizes (using same source for now)
cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
cp %{buildroot}/opt/%{full_name}/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png

# Create symlinks for system dictionaries if they exist
# Note: These are created at build time and packaged as symlinks
if [ -d /usr/share/hunspell ]; then
    ln -sf /usr/share/hunspell %{buildroot}/opt/%{full_name}/dictionaries
fi
if [ -d /usr/share/hyphen ]; then
    ln -sf /usr/share/hyphen %{buildroot}/opt/%{full_name}/hyphenation
fi

%post
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%postun
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{full_name}.png
%{_bindir}/%{full_name}
/opt/%{full_name}/

%changelog
* Thu Sep 26 2024 itexpert120 <itexpert120@example.com> - 0.4.12.1-1
- Initial package for Helium Browser
