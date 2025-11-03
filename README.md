# EV Charger Integration for Home Assistant

This integration allows you to monitor your EV charger from Home Assistant.

## Features

- Monitor charging status and parameters
- Real-time voltage, current, and power measurements
- Temperature monitoring
- Energy consumption tracking

## Installation

### HACS (Recommended)

1. Ensure HACS is installed
2. Add this repository as a custom repository in HACS
3. Search for "EV Charger" in HACS and install it
4. Restart Home Assistant
5. Add integration via Settings → Devices & Services → Add Integration

### Manual

Copy the `ev_charger` folder to your `custom_components` directory.

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "EV Charger"
4. Enter your email and password used in the EV Charger app

## Sensors

The integration creates the following sensors:

### Hardware Sensors
- Online status
- Charging status
- Hardware name

### Bluetooth Sensors
- Charging status
- Voltage (L1)
- Current (L1)
- Maximum current
- Set current
- Charge power
- Charged energy
- Historical energy
- Charge time
- Temperatures
- And more...

## Support

If you have any issues, please create an issue in the GitHub repository.