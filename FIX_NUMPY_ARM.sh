#!/bin/env bash

set -e

# Function to check if symbolic links for a package exist
check_symlinks() {
    local package_name="$1"
    local directory="$HOME/venv/lib/python3.9/site-packages"
    local sys_dir="/usr/lib/python3/dist-packages"

    # Check if symbolic links exist for the package
    if ls "$directory/$package_name"* 1> /dev/null 2>&1 ; then
        echo "Symbolic links for $package_name already exist in $directory. Skipping."
    else
        ln -s "$sys_dir/$package_name"* "$directory/" || echo "Can't create symbolic links"
    fi
}

# Step 1: Install system package python3-numpy from Debian's repositories
echo "Installing system package python3-numpy..."
sudo apt-get update || echo "Can't update package list"
sudo apt-get install -y python3-numpy python3-pandas python3-scipy python3-matplotlib || echo "Can't install packages"

# Step 2: Activate virtual environment at '../venv' path
echo "Activating virtual environment..."
source ../venv/bin/activate || echo "Can't activate virtual environment"

# Step 3: Uninstall numpy package from virtual environment
echo "Uninstalling numpy package from virtual environment..."
pip uninstall -y numpy || echo "Can't uninstall numpy package"
pip uninstall -y pandas || echo "Can't uninstall pandas package"
pip uninstall -y scipy || echo "Can't uninstall scipy package"
pip uninstall -y matplotlib || echo "Can't uninstall matplotlib package"

# Step 4: Create symbolic links from system python3-numpy to virtual environment
echo "Creating symbolic links..."
check_symlinks numpy
check_symlinks pandas
check_symlinks scipy
check_symlinks matplotlib
ln -s /usr/lib/python3/dist-packages/mpl_toolkits/* "$HOME/venv/lib/python3.9/site-packages/mpl_toolkits/" || echo "Can't create symbolic links"

echo "Fixing NumPy issue completed successfully!"
