#!/bin/env bash

# Define the configuration file
CONFIG_FILE="config.py"

# Function to prompt the user for a configuration value
prompt_config_value() {
    local prompt="$1"
    local default_value="$2"

    # If a default value is provided, display it in the prompt
    if [ -n "$default_value" ]; then
        read -rp "$prompt [$default_value]: " user_input
    else
        read -rp "$prompt: " user_input
    fi

    # Use the default value if the user input is empty
    if [ -z "$user_input" ]; then
        echo "$default_value"
    else
        echo "$user_input"
    fi
}

# Function to create directory if it doesn't exist
create_directory_if_not_exists() {
    local directory=$1

    if [ ! -d "$directory" ]; then
        mkdir -p "$directory"
        echo "Created directory: $directory"
    fi
}

# Prompt the user for each configuration value
echo "Configuration setup"
echo "-------------------"
echo "Please provide values for the following configuration options:"
echo "[Enter] for default value"
echo ""

# DEBUG
DEBUG=$(prompt_config_value "DEBUG" "True")

# SHOW_GRID
SHOW_GRID=$(prompt_config_value "SHOW_GRID" "True")

# FILTER_WSIZE
FILTER_WSIZE=$(prompt_config_value "FILTER_WSIZE" "15")

# REAL_CAPTURE
REAL_CAPTURE=$(prompt_config_value "REAL_CAPTURE" "False")

# EXAMPLE_DATA
EXAMPLE_DATA=$(prompt_config_value "EXAMPLE_DATA" "data4.csv")

# EXAMPLE_DATA_DIR
EXAMPLE_DATA_DIR=$(prompt_config_value "EXAMPLE_DATA_DIR" "./tpl")
create_directory_if_not_exists "$EXAMPLE_DATA_DIR"

# COLORS (Skipping as it's not user-configurable)

# CLR_NAMES (Skipping as it's not user-configurable)

# CLR_DICT (Skipping as it's not user-configurable)

# ATTEMPT_POINT (Skipping as it's not user-configurable)

# DATE_POINT (Skipping as it's not user-configurable)

# CURRENT_DATE (Skipping as it's not user-configurable)

# TIME_UNITS (Skipping as it's not user-configurable)

# USB_DEVICE
USB_DEVICE=$(prompt_config_value "USB_DEVICE" "sdb")

# USB_PART (Skipping as it's not user-configurable)

# WRITE_THRESHOLD
WRITE_THRESHOLD=$(prompt_config_value "WRITE_THRESHOLD" "100000")

# DATA_DIR_NAME
DATA_DIR_NAME=$(prompt_config_value "DATA_DIR_NAME" "data")

# REPORT_NAME
#REPORT_NAME=$(prompt_config_value "REPORT_NAME" "$(date +%Y-%m-%d)-{IDX}.pdf")

# TEMPLATE_FILE
TEMPLATE_FILE=$(prompt_config_value "TEMPLATE_FILE" "template2.pdf")

# LOG_FILE
LOG_FILE=$(prompt_config_value "LOG_FILE" "analyzer_reporter.log")

# Write the configuration values to the configuration file
cat <<EOF > "$CONFIG_FILE"
#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""
import os
from datetime import datetime


class Configuration(object):
    # Debugging
    DEBUG = $DEBUG

    # Plotting
    SHOW_GRID = $SHOW_GRID              # Show grid in plots
    TIME_UNITS = "ms"

    # Signal Processing
    FILTER_WSIZE = $FILTER_WSIZE

    # Data Capture
    REAL_CAPTURE = $REAL_CAPTURE          # Real capturing is not available yet
    EXAMPLE_DATA = "$EXAMPLE_DATA"    # Sample data instead of real capturing
    EXAMPLE_DATA_DIR = "$EXAMPLE_DATA_DIR"
    
    # Reporting
    ATTEMPT_POINT = (470, 767)    # XY point of attempt number in report canvas
    DATE_POINT = (470, 752)       # XY point of date in report canvas
    CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

    # USB Storage
    USB_DEVICE = "$USB_DEVICE"            # Change it to sda on Raspberry Pi
    USB_PART = USB_DEVICE + "1"
    USB_DRIVE = os.path.join("/dev", USB_PART)
    WRITE_TRESHOLD = $WRITE_THRESHOLD       # 100KB

    # Paths and Files
    DATA_DIR_NAME = "$DATA_DIR_NAME"
    IDX_STR = "{IDX}"
    REPORT_NAME = f'{CURRENT_DATE}-{IDX_STR}.pdf'
    TEMPLATE_FILE = os.path.join(os.path.abspath("$EXAMPLE_DATA_DIR"), "$TEMPLATE_FILE")
    LOG_FILE = os.path.join(os.path.dirname(__file__), "$LOG_FILE")

    # Colors Definition
    COLORS = [
        "#1f77b4",  #  1 blue
        "#ff7f0e",  #  2 orange
        "#2ca02c",  #  3 green
        "#d62728",  #  4 red
        "#9467bd",  #  5 purple
        "#8c564b",  #  6 brown
        "#e377c2",  #  7 pink
        "#bc8dd8",  #  8 violet
        "#bcbd22",  #  9 yellow
        "#17becf",  # 10 cyan
        "#7f7f7f",  # 11 gray
    ]
    CLR_NAMES = [
        "blue",
        "orange",
        "green",
        "red",
        "purple",
        "brown",
        "pink",
        "violet",
        "yellow",
        "cyan",
        "gray",
    ]
    CLR_DICT = dict(zip(CLR_NAMES, COLORS))

EOF

echo "Configuration setup completed. Configuration saved to $CONFIG_FILE"
