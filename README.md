# GTRI MERMAID – Maritime Environmental Remote Monitoring Acoustic Intelligent Device

**Senior Design Project – University of San Diego × Georgia Tech Research Institute (GTRI)**

This repository contains the code I wrote and field‑tested during the 2024‑2025 academic year.  Everything listed below reflects functionality that is currently working in the buoy prototypes.

---

## What the software really does

* **Dual‑channel capture** – records airborne (I²S MEMS) *and* underwater (USB hydrophone) audio at 48 kHz / 24‑bit.
* **Infrasound extraction** – real‑time FIR + FFT pipeline isolates < 20 Hz energy, logs SPL & peak frequency.
* **Lightweight event broadcast** – summary JSON packets sent once per second to a peer buoy over ad‑hoc Wi‑Fi.
* **Local storage** – raw WAV files written to SD card with automatic daily rotation.
* **Offline analysis tools** – Jupyter notebooks that generate spectrograms and statistical charts from field recordings.

---

## Hardware used in the prototype

| Part           | Model we used                       |
| -------------- | ----------------------------------- |
| Compute        | Raspberry Pi 4 Model B (2 GB)       |
| Air microphone | Adafruit SPH0645 I²S MEMS           |
| Connectivity   | Built‑in Wi‑Fi in ad‑hoc mode       |
| Power          | 10 Ah Li‑ion battery pack           |

If you swap components, just update `config.py` to match the new device names and sample rates.

---

## Quick‑start (on a Pi)

```bash
# Clone and enter project
$ git clone https://github.com/<your‑org>/mermaid.git
$ cd mermaid/pi

# Create and activate virtualenv
$ python3 -m venv venv && source venv/bin/activate

# Install dependencies (≈30 MB)
$ pip install -r requirements.txt

# Run the capture + broadcast loop
$ python main.py
```
