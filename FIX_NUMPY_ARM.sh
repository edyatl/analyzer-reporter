#!/bin/env bash

# The purpose of this script is to fix an issue with NumPy 
# on a Raspberry Pi ARM platform running Debian Bullseye. 

# The script achieves this goal by performing the following steps:

# 1. Install System Packages: The script updates the package list and 
# installs the required system packages (python3-numpy, python3-pandas, 
# python3-scipy, python3-matplotlib, python3-rpi.gpio, python3-gpiozero) 
# from the Debian repositories using apt-get.

# 2. Activate Virtual Environment: The script activates the virtual environment 
# where the Python packages are installed.

# 3. Uninstall Packages from Virtual Environment: The script uninstalls the NumPy, 
# Pandas, SciPy, Matplotlib, RPi.GPIO, and gpiozero packages from the virtual 
# environment using pip uninstall.

# 4. Create Symbolic Links: It creates symbolic links from the system-installed 
# packages (python3-numpy, python3-pandas, python3-scipy, python3-matplotlib, 
# python3-rpi.gpio, python3-gpiozero) into the virtual environment's site-packages 
# directory using the ln command.

set -e

# Function to check if symbolic links for a package exist
check_symlinks() {
    local package_name="$1"
    local directory="$HOME/venv/lib/python3.9/site-packages"
    local sys_dir="/usr/lib/python3/dist-packages"

    # Check if symbolic links exist for the package
    if ls "$directory/$package_name"* >/dev/null 2>&1; then
        echo "Symbolic links for $package_name already exist in $directory. Skipping."
    else
        ln -s "$sys_dir/$package_name"* "$directory/" || echo "Can't create symbolic links"
    fi
}

# Step 1: Install system packages
install_system_packages() {
    echo "Installing system packages..."
    sudo apt-get update || { echo "Can't update package list"; exit 1; }
    sudo apt-get install -y python3-numpy python3-pandas python3-scipy python3-matplotlib python3-rpi.gpio python3-gpiozero || { echo "Can't install packages"; exit 1; }
}

# Step 2: Activate virtual environment
activate_virtualenv() {
    echo "Activating virtual environment..."
    source ../venv/bin/activate || { echo "Can't activate virtual environment"; exit 1; }
}

# Step 3: Uninstall packages from virtual environment
uninstall_packages() {
    local packages=("numpy" "pandas" "scipy" "matplotlib" "rpi.gpio" "gpiozero")

    echo "Uninstalling packages from virtual environment..."
    for package in "${packages[@]}"; do
        pip uninstall -y "$package" || echo "Can't uninstall $package package"
    done
}

# Step 4: Create symbolic links from system packages to virtual environment
create_symlinks() {
    local packages=("numpy" "pandas" "scipy" "matplotlib" "mpl_toolkits" "gpiozero" "RPi" "pigpio")

    echo "Creating symbolic links..."
    for package in "${packages[@]}"; do
        check_symlinks "$package"
    done
    ln -s /usr/lib/python3/dist-packages/mpl_toolkits/* "$HOME/venv/lib/python3.9/site-packages/mpl_toolkits/" || echo "Can't create symbolic links"
}

# Main script
install_system_packages
activate_virtualenv
uninstall_packages
create_symlinks

echo "Fixing NumPy issue completed successfully!"

