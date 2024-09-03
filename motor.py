"""
Motor Sports Club
This program is designed to interface with hardware components in a motor sports environment, specifically for monitoring and displaying data from various sensors and control systems. It reads real-time data from a connected serial device (such as a battery management system or motor controller) and presents this information in a user-friendly format on a web interface.
website: http://127.0.0.1:5010/
"""

__author__ = "Luoyan Wei (Laura)"

import serial
from flask import Flask, render_template, jsonify, request
import threading
import re
from collections import defaultdict

app = Flask(__name__)



# Global dictionary to hold parsed data
serial_data = {
    "pack_info": {
        "Pack Voltage": "N/A",
        "Pack Current": "N/A",
        "Pack SOC": "N/A",
        "BMS Version": "N/A"
    },
    "current_limits": {
        "30A_limit": "N/A",
        "10A_limit": "N/A"
    },
    "ic_data": defaultdict(lambda: {
        "PWM": "N/A",
        "Temperature": "N/A",
        "Resistance": "N/A",
        "cells": []
    })
}

def parse_serial_data(raw_data):
    """
    Parses the serial data line into a structured format.
    Expected formats:
    - Pack Voltage: 486.3V
    - Pack Current: 12.3A
    - Pack SOC: 80.0%
    - BMS V1.0
    - ICx Cellx Voltage: 4.3210 PWM: 32.1% Temperature: 25.0C Resistance: 16.32
    """
    # Regex patterns to match different types of data
    
    current_limit_match = re.match(r"Current Limit: ([\d\.]+)A,([\d\.]+)A", raw_data)
    pack_voltage_match = re.match(r"Pack Voltage: ([\d\.]+)V", raw_data)
    pack_current_match = re.match(r"Pack Current: ([\d\.]+)A", raw_data)
    pack_soc_match = re.match(r"Pack SOC: ([\d\.]+)%", raw_data)
    bms_version_match = re.match(r"BMS (V[\d\.]+)", raw_data)
    ic_cell_match = re.match(r"IC(\d+) Cell(\d+) Voltage: ([\d\.]+) PWM: ([\d\.]+)% Temperature: ([\d\.]+)C Resistance: ([\d\.]+)", raw_data)

    if pack_voltage_match:
        serial_data["pack_info"]["Pack Voltage"] = f"{pack_voltage_match.group(1)}V"
    elif pack_current_match:
        serial_data["pack_info"]["Pack Current"] = f"{pack_current_match.group(1)}A"
    elif pack_soc_match:
        serial_data["pack_info"]["Pack SOC"] = f"{pack_soc_match.group(1)}%"
    elif bms_version_match:
        serial_data["pack_info"]["BMS Version"] = bms_version_match.group(1)
    elif current_limit_match:
        serial_data["current_limits"]["30A_limit"] = f"{current_limit_match.group(1)}A"
        serial_data["current_limits"]["10A_limit"] = f"{current_limit_match.group(2)}A"
    elif ic_cell_match:
        try:
            ic_number = int(ic_cell_match.group(1))
            cell_number = int(ic_cell_match.group(2))
            voltage = float(ic_cell_match.group(3))
            pwm = float(ic_cell_match.group(4))
            temperature = float(ic_cell_match.group(5))
            resistance = float(ic_cell_match.group(6))

            # Initialize the IC dictionary if it doesn't exist
            if ic_number not in serial_data["ic_data"]:
                serial_data["ic_data"][ic_number] = {"cells": [], "PWM": None, "Temperature": None, "Resistance": None}

            # Store or update the cell data
            found_cell = False
            for cell in serial_data["ic_data"][ic_number]["cells"]:
                if cell["Cell"] == cell_number:
                    cell["Voltage"] = voltage
                    found_cell = True
                    break

            if not found_cell:
                serial_data["ic_data"][ic_number]["cells"].append({
                    "Cell": cell_number,
                    "Voltage": voltage
                })

            # Update PWM, Temperature, and Resistance
            serial_data["ic_data"][ic_number]["PWM"] = pwm
            serial_data["ic_data"][ic_number]["Temperature"] = temperature
            serial_data["ic_data"][ic_number]["Resistance"] = resistance

        except ValueError as e:
            print(f"Error parsing data: {e}. Raw data: {raw_data}")
    else:
        print(f"Invalid data format: {raw_data}")

def read_serial(port):
    global serial_data
    try:
        ser = serial.Serial(port, baudrate=115200, timeout=2, rtscts=True)
        while True:
            try:
                raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                if raw_data:
                    parse_serial_data(raw_data)
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                break
    except serial.SerialException as e:
        print(f"Could not open serial port: {e}")

@app.route('/')
def index():
    return render_template('index_v5.html')

@app.route('/data')
def get_data():
    return jsonify(dict(serial_data))

@app.route('/set_port', methods=['POST'])
def set_port():
    port = request.form['port']
    threading.Thread(target=read_serial, args=(port,), daemon=True).start()
    return jsonify({"status": "Serial port reading started", "port": port})

if __name__ == '__main__':
    app.run(port=5010, debug=True)