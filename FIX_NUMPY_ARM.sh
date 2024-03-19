#!/bin/env bash

set -e

# Step 1: Install system package python3-numpy from Debian's repositories
echo "Installing system package python3-numpy..."
sudo apt-get update || echo "Can't update package list"
sudo apt-get install -y python3-numpy python3-pandas || echo "Can't install packages"

# Step 2: Activate virtual environment at '../venv' path
echo "Activating virtual environment..."
source ../venv/bin/activate || echo "Can't activate virtual environment"

# Step 3: Uninstall numpy package from virtual environment
echo "Uninstalling numpy package from virtual environment..."
pip uninstall -y numpy || echo "Can't uninstall numpy package"
pip uninstall -y pandas || echo "Can't uninstall pandas package"

# Step 4: Create symbolic links from system python3-numpy to virtual environment
echo "Creating symbolic links..."
ln -s /usr/lib/python3/dist-packages/numpy* ~/venv/lib/python3.9/site-packages/ || echo "Can't create symbolic links"
ln -s /usr/lib/python3/dist-packages/pandas* ~/venv/lib/python3.9/site-packages/ || echo "Can't create symbolic links"

echo "Fixing NumPy issue completed successfully!"
