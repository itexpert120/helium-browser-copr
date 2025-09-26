#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PACKAGE_NAME="helium"
SPEC_FILE="${PACKAGE_NAME}.spec"
MOCK_CONFIG="fedora-42-x86_64"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_error "Command '$1' not found. Please install it first."
        exit 1
    fi
}

# Check required commands
print_status "Checking required commands..."
check_command "rpmbuild"
check_command "mock"
check_command "spectool"

# Get the script directory (parent of scripts directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

print_status "Project directory: $PROJECT_DIR"

# Check if spec file exists
if [[ ! -f "$PROJECT_DIR/$SPEC_FILE" ]]; then
    print_error "Spec file not found: $PROJECT_DIR/$SPEC_FILE"
    exit 1
fi

# Create rpmbuild directory structure
print_status "Setting up rpmbuild directory structure..."
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy spec file to SPECS
print_status "Copying spec file..."
cp "$PROJECT_DIR/$SPEC_FILE" ~/rpmbuild/SPECS/

# Copy source files to SOURCES
print_status "Copying source files..."
cp "$PROJECT_DIR/${PACKAGE_NAME}.desktop" ~/rpmbuild/SOURCES/
cp "$PROJECT_DIR/${PACKAGE_NAME}.sh" ~/rpmbuild/SOURCES/

# Download source tarball using spectool
print_status "Downloading source tarball..."
cd ~/rpmbuild/SPECS
spectool -g -R "$SPEC_FILE"

# Build source RPM
print_status "Building source RPM..."
rpmbuild -bs "$SPEC_FILE"

# Find the generated SRPM
SRPM_FILE=$(find ~/rpmbuild/SRPMS -name "${PACKAGE_NAME}*.src.rpm" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)

if [[ -z "$SRPM_FILE" ]]; then
    print_error "Could not find generated SRPM file"
    exit 1
fi

print_success "Source RPM created: $SRPM_FILE"

# Build with mock
print_status "Building RPM with mock (config: $MOCK_CONFIG)..."
mock -r "$MOCK_CONFIG" --rebuild "$SRPM_FILE"

# Find the built RPM files
RPM_DIR="/var/lib/mock/$MOCK_CONFIG/result"
if [[ -d "$RPM_DIR" ]]; then
    RPM_FILES=$(find "$RPM_DIR" -name "${PACKAGE_NAME}*.rpm" -not -name "*.src.rpm" | head -5)
    if [[ -n "$RPM_FILES" ]]; then
        print_success "Built RPM files:"
        echo "$RPM_FILES" | while read -r rpm; do
            echo "  $(basename "$rpm")"
        done

        # Copy RPMs to a convenient location
        print_status "Copying RPMs to ~/rpmbuild/RPMS/"
        mkdir -p ~/rpmbuild/RPMS/x86_64
        cp $RPM_DIR/${PACKAGE_NAME}*.rpm ~/rpmbuild/RPMS/x86_64/ 2>/dev/null || true

        MAIN_RPM=$(echo "$RPM_FILES" | grep -v debuginfo | head -1)
        RPM_NAME=$(basename "$MAIN_RPM")

        print_success "Build completed successfully!"
        echo
        print_status "=== INSTALLATION COMMANDS ==="
        echo -e "${GREEN}Install Helium:${NC}"
        echo "  sudo dnf install ~/rpmbuild/RPMS/x86_64/$RPM_NAME"
        echo "  # or"
        echo "  sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/$RPM_NAME"
        echo
        echo -e "${YELLOW}Uninstall Helium:${NC}"
        echo "  sudo dnf remove $PACKAGE_NAME"
        echo "  # or"
        echo "  sudo rpm -e $PACKAGE_NAME"
        echo
        print_status "=== FILES LOCATION ==="
        echo "  Source RPM: $SRPM_FILE"
        echo "  Built RPMs: ~/rpmbuild/RPMS/x86_64/"
        echo "  Mock results: $RPM_DIR"
    else
        print_warning "No RPM files found in mock result directory"
    fi
else
    print_warning "Mock result directory not found: $RPM_DIR"
fi

print_success "Script completed successfully!"