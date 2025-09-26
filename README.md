# Helium Browser COPR Package

[![Copr build status](https://copr.fedorainfracloud.org/coprs/itexpert120/helium/package/helium/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/itexpert120/helium/package/helium/)

This repository contains the RPM spec file and related files for packaging [Helium Browser](https://github.com/imputnet/helium) for Fedora via COPR.

## About Helium Browser

Helium is a Chromium-based web browser that focuses on privacy and performance. It provides:

- Built-in ad and tracker blocking with uBlock Origin
- No telemetry or analytics
- Based on Chromium with privacy enhancements
- Zero web requests on first launch

## Installation

### Via COPR Repository

```bash
# Enable the COPR repository
sudo dnf copr enable itexpert120/helium

# Install Helium Browser
sudo dnf install helium
```

### Manual Installation

Download the latest RPM from the [COPR builds page](https://copr.fedorainfracloud.org/coprs/itexpert120/helium/builds/) and install:

```bash
sudo dnf install helium-*.rpm
```

## Usage

After installation, you can launch Helium Browser:

- From the application menu
- From the command line: `helium`

## Package Details

- **Architecture**: x86_64 only
- **Supported Distributions**: Fedora 39+
- **License**: GPL-3.0-only
- **Installation Location**: `/opt/helium/`

## Contributing

### Building Locally

To test the package locally:

```bash
# Install build dependencies
sudo dnf install rpm-build rpmdevtools mock

# Build the source RPM
rpmbuild -bs helium.spec

# Test build with mock
mock -r fedora-41-x86_64 --rebuild helium-*.src.rpm
```

### Reporting Issues

- For issues with the Helium Browser itself: [Helium GitHub Issues](https://github.com/imputnet/helium/issues)
- For issues with this RPM package: [Package Issues](https://github.com/itexpert120/helium-browser-copr/issues)

## Acknowledgments

Thanks to [zen-browser-copr](https://github.com/ArchitektApx/zen-browser-copr) for the initial package structure.
