# analyzer-reporter - Python Logic Analyzer with Sigrok

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
- Python 3.x
- Required Python packages: numpy, matplotlib, scipy
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

## Configuration

The analyzer-reporter application can be configured to suit your specific requirements using the `config.py` file. This configuration file contains various parameters that control the behavior of the application. Below are the configurable options along with their descriptions:

### Debugging

- **DEBUG**: Set to `True` to enable debugging mode, which provides additional logging information for troubleshooting purposes.

### Plotting

- **SHOW_GRID**: Set to `True` to display gridlines on plots for better visualization.

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


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](./LICENSE) file for details.
