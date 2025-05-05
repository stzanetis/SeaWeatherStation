# Sea Weather Station

**Authors:** Iasonas Lamprinidis, Ioannis Michalainas, Savvas Tzanetis, Vasileios Zoidis  
**Date:** May 2025

This project implements a remote *weather station*. The premise is to use multiple Arduino devices to create a network of data nodes. These nodes will monitor temperature, pressure and estimated wave shore impact/height at sea level. Collected data will then be displayed in a web application, to be used by fishermen, researchers or hobbyists.

## Features

- Temperature and pressure measurement
- Wave characteristics estimation
- Real-time data visualization
- Web application dashboard

## Architecture

The project consists of three main components:
- **Arduino**: Data collection sensors and transmission modules
- **Backend**: Data processing, storage, and API services
- **Frontend**: Web interface for data visualization and analysis

## Tools & Technologies

- Arduino (hardware sensors and microcontrollers)
- Python (backend data processing)
- RF22 cards (wireless communication)
- Web technologies (frontend visualization)