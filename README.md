# Motor Sports Club

This project is designed to interface with hardware components in a motor sports environment, specifically for monitoring and displaying data from various sensors and control systems. The application reads real-time data from a connected serial device (such as a battery management system or motor controller) and presents this information in a user-friendly format on a web interface.

## Features

- **Real-Time Monitoring**: Reads and processes data from a connected serial device.
- **Web Interface**: Displays sensor data on a user-friendly web interface.
- **Data Parsing**: Supports parsing of various data formats, including voltage, current, SOC, temperature, and more.
- **Multithreaded Serial Reading**: Efficiently reads data from the serial port using multithreading.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/weiluoyan/MotorSportsClub.git
   cd MotorSportsClub
2. Install the required Python packages:(Make sure you have Python installed on your system.)

3. Run the Flask application:
       python motor.py
5. Access the web interface by navigating to:
    http://127.0.0.1:5010/
