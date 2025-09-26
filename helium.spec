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
echo "DEBUG: Starting prep section"
echo "DEBUG: PWD = $(pwd)"
echo "DEBUG: Contents before setup:"
ls -la || echo "DEBUG: ls failed"
%setup -q -c -n %{application_name}
echo "DEBUG: Contents after setup:"
ls -la || echo "DEBUG: ls failed after setup"
echo "DEBUG: Prep section completed"

%install
echo "DEBUG: Starting install section"
echo "DEBUG: buildroot = %{buildroot}"
echo "DEBUG: PWD = $(pwd)"
echo "DEBUG: Contents of current directory:"
ls -la || echo "DEBUG: ls failed in install"

rm -rf %{buildroot}
echo "DEBUG: Cleaned buildroot"

# Create directory structure
echo "DEBUG: Creating directory structure"
install -d %{buildroot}/opt/%{full_name} || echo "DEBUG: Failed to create /opt/%{full_name}"
install -d %{buildroot}%{_bindir} || echo "DEBUG: Failed to create %{_bindir}"
install -d %{buildroot}%{_datadir}/applications || echo "DEBUG: Failed to create applications dir"
install -d %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps || echo "DEBUG: Failed to create icon dirs"
echo "DEBUG: Directory structure created"

# Install all browser files
echo "DEBUG: Installing browser files to /opt/%{full_name}/"
echo "DEBUG: Files to copy:"
ls -la
cp -r * %{buildroot}/opt/%{full_name}/ || echo "DEBUG: Failed to copy browser files"
echo "DEBUG: Browser files copied"

# Install desktop file and wrapper script
echo "DEBUG: Installing desktop file and wrapper script"
echo "DEBUG: SOURCE1 = %{SOURCE1}"
echo "DEBUG: SOURCE2 = %{SOURCE2}"
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{full_name}.desktop || echo "DEBUG: Failed to install desktop file"
install -D -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/%{full_name} || echo "DEBUG: Failed to install wrapper script"
echo "DEBUG: Desktop file and wrapper script installed"

# Install icons at different sizes (using same source for now)
echo "DEBUG: Installing icons"
echo "DEBUG: Checking helium directory structure:"
ls -la %{buildroot}/opt/%{full_name}/ || echo "DEBUG: /opt/%{full_name}/ not found"
echo "DEBUG: Checking if helium subdirectory exists:"
ls -la %{buildroot}/opt/%{full_name}/helium/ || echo "DEBUG: helium subdirectory not found"
echo "DEBUG: Looking for any .png files in buildroot:"
find %{buildroot}/opt/%{full_name}/ -name "*.png" -type f || echo "DEBUG: No .png files found in buildroot"

# Try different possible locations for the icon
ICON_SOURCE=""
if [ -f %{buildroot}/opt/%{full_name}/helium/product_logo_256.png ]; then
    ICON_SOURCE="%{buildroot}/opt/%{full_name}/helium/product_logo_256.png"
    echo "DEBUG: Found icon in helium subdirectory"
elif [ -f %{buildroot}/opt/%{full_name}/product_logo_256.png ]; then
    ICON_SOURCE="%{buildroot}/opt/%{full_name}/product_logo_256.png"
    echo "DEBUG: Found icon in root directory"
else
    echo "DEBUG: Icon not found, looking for any PNG files to use"
    ICON_SOURCE=$(find %{buildroot}/opt/%{full_name}/ -name "*logo*.png" -type f | head -1)
    if [ -n "$ICON_SOURCE" ]; then
        echo "DEBUG: Using alternative icon: $ICON_SOURCE"
    else
        echo "DEBUG: No suitable icon found"
    fi
fi

if [ -n "$ICON_SOURCE" ] && [ -f "$ICON_SOURCE" ]; then
    echo "DEBUG: Copying icon from $ICON_SOURCE"
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png || echo "DEBUG: Failed to copy 128x128 icon"
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png || echo "DEBUG: Failed to copy 64x64 icon"
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png || echo "DEBUG: Failed to copy 48x48 icon"
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png || echo "DEBUG: Failed to copy 32x32 icon"
    cp "$ICON_SOURCE" %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png || echo "DEBUG: Failed to copy 16x16 icon"
else
    echo "DEBUG: CRITICAL: No icon source available for installation"
fi
echo "DEBUG: Icons installed"

# Create symlinks for system dictionaries if they exist
echo "DEBUG: Creating dictionary symlinks"
# Note: These are created at build time and packaged as symlinks
if [ -d /usr/share/hunspell ]; then
    echo "DEBUG: Creating hunspell symlink"
    ln -sf /usr/share/hunspell %{buildroot}/opt/%{full_name}/dictionaries || echo "DEBUG: Failed to create hunspell symlink"
else
    echo "DEBUG: /usr/share/hunspell not found"
fi
if [ -d /usr/share/hyphen ]; then
    echo "DEBUG: Creating hyphen symlink"
    ln -sf /usr/share/hyphen %{buildroot}/opt/%{full_name}/hyphenation || echo "DEBUG: Failed to create hyphen symlink"
else
    echo "DEBUG: /usr/share/hyphen not found"
fi
echo "DEBUG: Install section completed"

%post
echo "DEBUG: Running post section"
echo "DEBUG: Updating icon cache"
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || echo "DEBUG: Icon cache update failed in post"
echo "DEBUG: Post section completed"

%postun
echo "DEBUG: Running postun section"
echo "DEBUG: Updating icon cache"
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || echo "DEBUG: Icon cache update failed in postun"
echo "DEBUG: Postun section completed"

%files
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{full_name}.png
%{_bindir}/%{full_name}
/opt/%{full_name}/

%changelog
* Thu Sep 26 2024 itexpert120 <itexpert120@example.com> - 0.4.12.1-1
- Initial package for Helium Browser
