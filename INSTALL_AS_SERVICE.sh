#!/bin/env bash

set -e

# Check if running as root or with sudo
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root or with sudo."
    exit 1
fi

# Change directory to the location of the script
cd "$(dirname "$0")" || exit 1

# Get basename of current directory
BASENAME=$(basename "$PWD") || exit 1

# Change directory to parent directory
cd .. || exit 1

# Get the absolute path of the analyzer-reporter directory
ANALYZER_REPORTER_BASE_DIR=$(pwd) || exit 1

# Change directory back the location of the script
cd - || exit 1

# Copy the service file to /etc/systemd/system
sed "s|/home/operator|$ANALYZER_REPORTER_BASE_DIR|g" analyzer_reporter.service | \
sed "s|$ANALYZER_REPORTER_BASE_DIR/analyzer-reporter|$ANALYZER_REPORTER_BASE_DIR/$BASENAME|g" > /etc/systemd/system/analyzer.service || exit 1

# Reload systemd daemon
systemctl daemon-reload || exit 1

# Enable and start the analyzer service
systemctl enable analyzer.service || exit 1
systemctl start analyzer.service || exit 1

echo "Analyzer Reporter service has been installed and started."

