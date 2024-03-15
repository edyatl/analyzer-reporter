#!/bin/env bash

# Check if virtualenv is installed, install if not
if ! command -v virtualenv &> /dev/null; then
    echo "Installing virtualenv..."
    sudo apt-get update
    sudo apt-get install -y virtualenv
fi

# Create virtual environment
echo "Creating virtual environment..."
virtualenv -p python3 ../venv

# Activate virtual environment
echo "Activating virtual environment..."
source ../venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "Installation completed successfully."
    read -rp "Do you want to configure the application now? [Y/n]: " configure_choice
    if [[ $configure_choice == "Y" || $configure_choice == "y" ]]; then
        echo "Running CONFIGURE.sh..."
        bash CONFIGURE.sh
    else
        echo "Please run CONFIGURE.sh manually before using the application."
    fi
else
    echo "Error: Installation failed. Please check the error messages above."
fi

