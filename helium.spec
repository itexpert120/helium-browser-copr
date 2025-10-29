%global             full_name helium
%global             application_name helium
%global             debug_package %{nil}

Name:               helium
Version:            null
Release:            1%{?dist}
Summary:            Private, fast, and honest web browser

License:            GPL-3.0-only
URL:                https://github.com/imputnet/helium
Source0:            https://github.com/imputnet/helium-linux/releases/download/null/helium-null-x86_64_linux.tar.xz
Source1:            %{full_name}.desktop
Source2:            %{full_name}.sh
Source3:            product_logo_256.png

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
Requires:           qt5-qtbase
Requires:           qt6-qtbase
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
# Flatten the extracted top-level directory into ./helium so we end up with a
# folder named "helium" containing the app files (not a nested versioned dir)
if ls helium-*-x86_64_linux >/dev/null 2>&1; then
    cp -a helium-*-x86_64_linux/. .
    rm -rf helium-*-x86_64_linux
fi

%install
rm -rf %{buildroot}

# Create directory structure
install -d %{buildroot}/opt
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps

# Install the "helium" folder into /opt as /opt/helium
cp -a %{application_name} %{buildroot}/opt/%{full_name}

# Install desktop file and wrapper script
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{full_name}.desktop
install -D -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/%{full_name}

# Install icons – prefer the packaged logo PNG, fallback to discovered one
ICON_SOURCE="%{SOURCE3}"
if [ ! -f "$ICON_SOURCE" ]; then
if [ -f %{buildroot}/opt/%{full_name}/product_logo_256.png ]; then
    ICON_SOURCE="%{buildroot}/opt/%{full_name}/product_logo_256.png"
else
    ICON_SOURCE=$(find %{buildroot}/opt/%{full_name}/ -name "*logo*.png" -type f | head -1)
    fi
fi

if [ -n "$ICON_SOURCE" ] && [ -f "$ICON_SOURCE" ]; then
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
fi

# Create symlinks for system dictionaries if they exist
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
* Wed Oct 29 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - null
- Update to upstream release null

* Sat Oct 25 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - 0.5.8.1
- Update to upstream release 0.5.8.1

* Sun Oct 19 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - 0.5.7.1
- Update to upstream release 0.5.7.1

* Thu Oct 16 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - 0.5.6.1
- Update to upstream release 0.5.6.1

* Sat Oct 11 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - 0.5.5.2
- Update to upstream release 0.5.5.2

* Thu Oct 09 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - 0.5.5.1
- Update to upstream release 0.5.5.1

* Wed Oct 08 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - 0.5.3.1
- Update to upstream release 0.5.3.1

* Tue Oct 07 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - 0.5.2.1
- Update to upstream release 0.5.2.1

* Tue Oct 07 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - null
- Update to upstream release null

* Mon Oct 06 2025 Muhammad Zeeshan Ahmad <itexpert120@outlook.com> - 0.5.2.1
- Update to upstream release 0.5.2.1

* Thu Sep 26 2024 itexpert120 <itexpert120@example.com> - 0.4.12.1-1
- Initial package for Helium Browser
