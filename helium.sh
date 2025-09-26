#!/bin/bash
# Helium Browser wrapper script

# Set the path to the Helium installation directory
HELIUM_DIR="/opt/helium"

# Set environment variables (similar to chrome-wrapper)
export CHROME_WRAPPER=$(readlink -f "$0")
export CHROME_DESKTOP="helium.desktop"

# Set library path to use bundled libraries
export LD_LIBRARY_PATH="$HELIUM_DIR:$HELIUM_DIR/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"

# Custom version string for this release
export CHROME_VERSION_EXTRA="helium"

# Call chrome directly to avoid chrome-wrapper creating chromium-devel.desktop
exec "$HELIUM_DIR/chrome" --class="helium" "$@"