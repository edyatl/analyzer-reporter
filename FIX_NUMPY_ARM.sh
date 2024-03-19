#!/bin/env bash

set -e

# Function to check if symbolic links for a package exist
check_symlinks() {
    package_name="$1"
    directory="~/venv/lib/python3.9/site-packages/"
    sys_dir="/usr/lib/python3/dist-packages/"

    # Check if symbolic links exist for the package
    if [ -e "$directory/$package_name"* ]; then
        echo "Symbolic links for $package_name already exist in $directory. Skipping."
    else
        ln -s "$sys_dir/$package_name"* "$directory"
    fi
}

# Step 1: Install system package python3-numpy from Debian's repositories
echo "Installing system package python3-numpy..."
sudo apt-get update || echo "Can't update package list"
sudo apt-get install -y python3-numpy python3-pandas python3-scipy || echo "Can't install packages"

# Step 2: Activate virtual environment at '../venv' path
echo "Activating virtual environment..."
source ../venv/bin/activate || echo "Can't activate virtual environment"

# Step 3: Uninstall numpy package from virtual environment
echo "Uninstalling numpy package from virtual environment..."
pip uninstall -y numpy || echo "Can't uninstall numpy package"
pip uninstall -y pandas || echo "Can't uninstall pandas package"
pip uninstall -y scipy || echo "Can't uninstall pandas package"

# Step 4: Create symbolic links from system python3-numpy to virtual environment
echo "Creating symbolic links..."
check_symlinks numpy || echo "Can't create symbolic links"
check_symlinks pandas || echo "Can't create symbolic links"
check_symlinks scipy || echo "Can't create symbolic links"

echo "Fixing NumPy issue completed successfully!"
