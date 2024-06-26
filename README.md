# analyzer-reporter - Python Logic Analyzer

This Python program turns your Raspberry Pi into a logic analyzer using the [Hantek 4032L](https://sigrok.org/wiki/Hantek_4032L) USB-based 32-channel logic analyzer and [Sigrok software](https://sigrok.org/wiki/Main_Page). It allows you to capture signals, filter noise, measure pulse widths, plot signals, and save reports as PDF files on a USB flash drive.

## Features

- Capture signals from Hantek 4032L logic analyzer using Sigrok software
- Filter noise from captured signals
- Measure pulse widths of signals
- Plot captured signals
- Save reports as PDF files on a USB flash drive

## Requirements

- Raspberry Pi
- Hantek 4032L USB-based 32-channel logic analyzer
- Sigrok software
- Python 3.x (Developed and tested on 3.9 and 3.11)
- Required Python packages: numpy, pandas, matplotlib, scipy, reportlab, pypdf, RPi.GPIO, gpiozero
- Physical button and LED lamp connected to Raspberry Pi GPIO pins
- USB flash drive

## Files Description

```
.
├── CONFIGURE.sh
├── FIX_NUMPY_ARM.sh
├── INSTALL.sh
├── INSTALL_AS_SERVICE.sh
├── __init__.py
├── analyzer_controller.py
├── analyzer_reporter.py
├── analyzer_reporter.service
├── analyzer_report.ipynb
├── config.py
├── logger.py
├── report_generator.py
├── requirements.txt
├── signal_grapher.py
├── signal_processor.py
└── storage_controller.py

```

- **[CONFIGURE.sh](CONFIGURE.sh)**: Bash script used to configure the application settings interactively.
  
- **[FIX_NUMPY_ARM.sh](FIX_NUMPY_ARM.sh)**: Bash script to fix issues with NumPy on ARM platforms, such as Raspberry Pi.

- **[INSTALL.sh](INSTALL.sh)**: Bash script for installing the application and its dependencies.

- **[INSTALL_AS_SERVICE.sh](INSTALL_AS_SERVICE.sh)**: Bash script to install the application as a systemd service for automatic startup.

- **[\_\_init\_\_.py](__init__.py)**: Initialization file for the Python package.

- **[analyzer_controller.py](analyzer_controller.py)**: Python module containing the AnalyzerController class for capturing signals from an analyzer.

- **[analyzer_report.ipynb](analyzer_report.ipynb)**: Jupyter Notebook file with examples and documentation for the **analyzer-reporter** application.

- **[analyzer_reporter.py](analyzer_reporter.py)**: Main Python script for running the **analyzer-reporter** application.

- **[analyzer_reporter.service](analyzer_reporter.service)**: Systemd service unit file for running the application as a background service.

- **[config.py](config.py)**: Python module containing the Configuration class with application settings and configurations.

- **[logger.py](logger.py)**: Python module for logging messages and events during application execution.

- **[report_generator.py](report_generator.py)**: Python module for generating reports based on captured signals.

- **[requirements.txt](requirements.txt)**: Text file listing the Python packages required by the application.

- **[signal_grapher.py](signal_grapher.py)**: Python module for plotting and visualizing signal data.

- **[signal_processor.py](signal_processor.py)**: Python module for processing and analyzing captured signals.

- **[storage_controller.py](storage_controller.py)**: Python module for managing storage devices and data directories.


## Installation

Follow these steps to install and configure the **analyzer-reporter** Python application on your system.

#### Step 1: Clone the Repository

Clone the **analyzer-reporter** repository from GitHub and navigate to the project directory:

```bash
git clone https://github.com/edyatl/analyzer-reporter.git
cd analyzer-reporter
```

#### Step 2: Run the Installation Script

Execute the `INSTALL.sh` script to set up the virtual environment and install the required Python packages:

```bash
bash INSTALL.sh
```

This script will create a virtual environment, activate it, and install all necessary dependencies specified in the `requirements.txt` file. Follow the prompts to configure the application settings.

#### Step 3: Provide Configuration Values

The installation script will prompt you to provide configuration values for various options. You can either accept the default values or enter custom values as per your requirements.

#### Step 4: Prepare Example Data and Template

Copy the example data file `data.csv` and the template PDF file `template.pdf` to the `tpl/` directory created during the configuration step.

```bash
cp /path/to/data.csv tpl/
cp /path/to/template.pdf tpl/
```

If you don't have a template PDF file, the application will use a blank A4 page as the template.

#### Step 5: Fix NumPy Issue (If Required)

If you are using a Raspberry Pi or ARM platform, execute the `FIX_NUMPY_ARM.sh` script to fix any issues with NumPy:

```bash
bash FIX_NUMPY_ARM.sh
```

#### Step 6: Activate Virtual Environment

Activate the virtual environment before running the application:

```bash
source ../venv/bin/activate
```

#### Step 7: Test the Application

Test the application to ensure everything is working correctly. If you are not using a Raspberry Pi, run the following command with GPIO mock:

```bash
GPIOZERO_PIN_FACTORY=mock python analyzer_reporter.py
```

If you are using a Raspberry Pi, run the application without GPIO mocking:

```bash
python analyzer_reporter.py
```

Press `Ctrl + C` to exit the application.

>**Note:** When testing the application, it's recommended to start with the `DEBUG` mode enabled (`DEBUG=True`) and `REAL_CAPTURE` set to `False`. This configuration allows for verbose logging and detailed output, which can be helpful for identifying any issues during testing. Once the application functions correctly with example data and mock GPIO interactions, users can switch `REAL_CAPTURE` to `True` to enable real signal capturing. Finally, set `DEBUG=False` to reduce verbose logging and standard output once real capturing is verified.

#### Step 8: Install as Systemd Service (Optional)

To install the **analyzer-reporter** application as a systemd service for automatic startup, run the following script:

```bash
sudo bash INSTALL_AS_SERVICE.sh
```

This script will copy the service unit file to `/etc/systemd/system/` and start the service. The application will now run in the background as a service.

#### Step 9: Verify Installation

Check the status of the installed service to ensure it's running without any errors:

```bash
sudo systemctl status analyzer.service
```

If the service is active and running, the installation process is complete.

You have successfully installed and configured the **analyzer-reporter** Python application on your system. You can now use it to capture, process, and generate reports for your analyzer data.


#### Step 10: Connect hardware

1. Connect the Hantek 4032L logic analyzer to your Raspberry Pi.
2. Install Sigrok software on your Raspberry Pi.
3. Connect the physical button and LED lamp to the GPIO pins of your Raspberry Pi.

## Usage

1. Run the Python program on your Raspberry Pi.
2. Press the physical button to capture signals.
3. LED lamp will blink to indicate capturing or waiting for storage modes of the program. 
4. LED lamp will on to indicate waiting for button press mode.
5. Reports will be saved as PDF files on the USB flash drive with the current date and index of the attempt.

>**Notes:**
>- **Familiarize with the Jupyter Notebook**: Before using the analyzer-reporter application, we strongly encourage users to familiarize themselves with the [analyzer_report.ipynb](analyzer_report.ipynb) Jupyter Notebook file. This notebook provides detailed descriptions of all application classes, examples of their usage, generated graphs, and the general logic of the application. It serves as a comprehensive guide to understanding the functionality and capabilities of the analyzer-reporter.
>- **Customize for Different Devices**: Although the analyzer-reporter application is designed to interact with the Hantek 4032L logic analyzer by default, it can easily be modified to work with other devices supported by Sigrok. To do this, users can edit the configuration file and specify the desired driver and parameters for the `sigrok-cli` command. This flexibility allows users to adapt the application to their specific hardware requirements and preferences.
>- **Versatile Use Cases**: While the application was initially designed to run as a service on Raspberry Pi, it can also be used on a PC without modification. Additionally, individual modules of the application classes can be utilized independently for specific tasks or integrated into other projects. Users can modify the entry point of the application to customize its behavior or integrate it into their existing workflows as needed.

## Configuration

The analyzer-reporter application can be configured to suit your specific requirements using the `config.py` file. This configuration file contains various parameters that control the behavior of the application. Below are the configurable options along with their descriptions:

### Debugging

- **DEBUG**: Set to `True` to enable debugging mode, which provides additional logging information for troubleshooting purposes.

### Plotting

- **SHOW_GRID**: Set to `True` to display gridlines on plots for better visualization.
- **PLOT_WIDTH**: Control the plotting behavior regarding pulse widths. It can take values `"all"`, `"rising"`, `"falling"`, or `None`.

### GPIO Pin Numbers

- **LED_PIN**: GPIO pin number for controlling the LED indicator.
- **BUTTON_PIN**: GPIO pin number for the button input.

### Interface

- **BLINK_TIME**: Duration (in seconds) for LED blinking.
- **BUTTON_TIMEOUT**: Timeout (in seconds) for button press detection.

### Signal Processing

- **FILTER_WSIZE**: Window size for signal filtering.

### Data Capture

- **REAL_CAPTURE**: Set to `True` to enable real signal capturing. Set to `False` to use example data.
- **EXAMPLE_DATA**: Specifies the filename of the example data to be used if real capturing is not available (if `REAL_CAPTURE` is set to `False`).
- **EXAMPLE_DATA_DIR**: Directory path for storing example data files.

### Reporting

- **ATTEMPT_POINT**: XY coordinates of the attempt number in the report canvas.
- **DATE_POINT**: XY coordinates of the date in the report canvas.
- **CURRENT_DATE**: Current date in YYYY-MM-DD format.

### USB Storage

- **USB_DEVICE**: USB device identifier.
- **WRITE_THRESHOLD**: Threshold (in bytes) for USB storage write operations.

### Paths and Files

- **DATA_DIR_NAME**: Name of the directory for storing reports files.
- **REPORT_NAME**: Format for naming report files.
- **TEMPLATE_FILE**: Path to the template PDF file for report generation.
- **LOG_FILE**: Path to the log file for storing application logs.

### Colors Definition

- **COLORS**: List of color codes for plotting.
- **CLR_NAMES**: List of color names for reference.
- **CLR_DICT**: Dictionary mapping color names to color codes.

## Changelog

### Version 0.1.1 (April 7, 2024)

#### SignalProcessor:
- Added new property `rising_signals` to determine rising signals within each signal.
- Refactored the `_filter_noise` method to use the `apply` function for improved performance.
- Refactored the `_find_pulse_pivots` method to utilize the `apply` function for better efficiency.
- Updated the `_calculate_pulse_metrics` method to directly compute pulse points and widths, resulting in a more streamlined approach.
- Introduced the `_determine_rising_signals` method to determine rising signals based on pulse pivots.
- Replaced the `_signal_pulse_count` and `_signal_pulse_width` methods with `_signal_pulse_points_width` for unified calculation of pulse points and widths.
- Implemented the `_is_start_from_pulse` method to check if a signal starts from a pulse for accurate determination of pulse points and widths.
- Introduced the `_is_rising_signal` method to determine if a signal is rising based on its pulse pivots.

These changes enhance signal processing capabilities, improve code efficiency, and provide more accurate analysis of signal characteristics, including pulse points, widths, and rising signals.


#### SignalGrapher:
- Added a new parameter `rising_signals` to the constructor to incorporate information about rising signals.
- Introduced the `_get_signals_to_plot` method to determine which signals to plot based on the `cfg.PLOT_WIDTH` configuration variable.
- Modified the `plot_signals` method to plot signals and pulses based on the selected signals to plot according to their rising or falling nature, as specified by the `cfg.PLOT_WIDTH` configuration.
- Enhanced flexibility by allowing plotting of all signals, only rising signals, or only falling signals based on the `cfg.PLOT_WIDTH` configuration.
- Updated the initialization process to accommodate the `rising_signals` parameter.
- Adjusted internal logic to ensure proper plotting of signals according to the selected criteria.

These changes provide improved control over which signals to plot and enhance the visualization of signals and pulses based on their rising or falling characteristics, thereby facilitating more insightful analysis of the data.

#### Configuration:
- Added new attribute `PLOT_WIDTH` to control the plotting behavior regarding pulse widths. It can take values `"all"`, `"rising"`, `"falling"`, or `None`.


#### analyzer_reporter.py:
- Updated entry point to accommodate changes in SignalProcessor and SignalGrapher.
- Adjusted functionality to reflect modifications made in both classes.


## Useful Sigrok Links

Sigrok is a powerful open-source signal analysis software suite that supports various hardware devices for capturing, decoding, and analyzing signals. Below are some useful links related to Sigrok:

- **Official Sigrok Website**: [sigrok.org](https://sigrok.org/)
  - The official website of Sigrok provides comprehensive documentation, downloads, and resources for users interested in using Sigrok for signal analysis.

- **Supported Devices**: [sigrok.org/wiki/Supported_hardware](https://sigrok.org/wiki/Supported_hardware)
  - This page lists the hardware devices supported by Sigrok, including oscilloscopes, logic analyzers, multimeters, and more. You can check if your device is compatible with Sigrok here.

- **Download Sigrok**: [sigrok.org/downloads/](https://sigrok.org/downloads/)
  - Visit this page to download the latest version of the Sigrok software suite for your operating system. Sigrok is available for various platforms, including Linux, Windows, and macOS.

These links provide valuable resources for learning more about Sigrok, troubleshooting issues, and connecting with the Sigrok community. Whether you're a beginner or an experienced user, Sigrok offers a wide range of tools and support for your signal analysis needs.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](./LICENSE) file for details.
