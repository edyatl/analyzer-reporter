# Python Logic Analyzer with Sigrok

This Python program turns your Raspberry Pi into a logic analyzer using the Hantek 4032L USB-based 32-channel logic analyzer and Sigrok software. It allows you to capture signals, filter noise, measure pulse widths, plot signals, and save reports as PDF files on a USB flash drive.

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

## Installation

1. Connect the Hantek 4032L logic analyzer to your Raspberry Pi.
2. Install Sigrok software on your Raspberry Pi.
3. Connect the physical button and LED lamp to the GPIO pins of your Raspberry Pi.
4. Clone this GitHub repository to your Raspberry Pi.

## Usage

1. Run the Python program on your Raspberry Pi.
2. Press the physical button to start capturing signals.
3. LED lamp will blink to indicate the availability of the program.
4. Press the button again to stop capturing signals.
5. Reports will be saved as PDF files on the USB flash drive with the current date and index of the attempt.

## Configuration

- Modify the GPIO pin numbers in the Python program according to your setup.
- Adjust the signal capture settings in the Python program as needed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](LICENSE)
