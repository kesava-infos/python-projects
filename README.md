# Sound Amplifier
# Real-Time Sound Amplifier with Noise Reduction (Python)

This project is a **real-time audio amplification and monitoring application**
built in Python. It captures microphone input, applies gain (amplification) and
optional noise reduction, and plays the processed audio through a selected
output device. A Tkinter-based graphical interface allows real-time control.

---

## Table of Contents

- Overview
- Key Features
- Technology Stack
- System Architecture
- Audio Configuration
- Global State Management
- Audio Processing Pipeline
- Threading Model
- Device Enumeration
- Graphical User Interface
- Application Flow
- Performance Considerations
- Limitations
- Future Improvements
- How to Run

---

## Overview

The application functions as a **live audio pass-through system**. Audio is
captured from a microphone, processed using digital signal processing (DSP),
and immediately routed to speakers or headphones with minimal latency.

This type of system is commonly used in:
- Assistive listening devices
- Real-time monitoring
- Audio testing and diagnostics
- DSP demonstrations

---

## Key Features

- Real-time microphone monitoring
- Adjustable audio amplification (gain)
- Optional stationary noise reduction
- Selectable input and output devices
- Low-latency callback-based audio streaming
- Responsive GUI with background audio thread

---

## Technology Stack

| Component | Purpose |
|---------|--------|
| `sounddevice` | Real-time audio input/output |
| `numpy` | Numerical audio processing |
| `noisereduce` | Noise suppression algorithms |
| `threading` | Background audio execution |
| `tkinter / ttk` | Graphical user interface |

---

## System Architecture

The application is divided into three logical layers:


1. Imported Libraries
import sounddevice as sd
import numpy as np
import noisereduce as nr
import threading
import tkinter as tk
from tkinter import ttk


Purpose of each library:

sounddevice
Handles real-time audio input/output using the system’s audio devices.

numpy
Used for numerical operations on audio buffers (gain, clipping).

noisereduce
Provides DSP algorithms for noise suppression.

threading
Runs the audio processing loop in a background thread so the GUI remains responsive.

tkinter / ttk
Creates the graphical user interface (dropdowns, sliders, buttons).

2. Audio Configuration
CHANNELS = 1
BLOCK_SIZE = 1024


CHANNELS = 1
Mono audio (one microphone channel).

BLOCK_SIZE = 1024
Number of samples processed per callback invocation.
Smaller values → lower latency, higher CPU usage.

3. Global State Variables
running = False
gain_value = 2.0
noise_reduction_enabled = True
stream = None


These variables control application state:

running – Starts/stops audio processing

gain_value – Amplification multiplier

noise_reduction_enabled – Enables/disables noise suppression

stream – Placeholder for the audio stream object

input_device = None
output_device = None
SAMPLE_RATE = None


Selected audio devices and their sample rate

Sample rate is retrieved dynamically from the input device

4. Audio Processing Loop
audio_loop() function

This function runs in a background thread and manages the audio stream.

device_info = sd.query_devices(input_device)
SAMPLE_RATE = int(device_info['default_samplerate'])


Queries the selected input device

Uses its native sample rate to avoid resampling issues

Audio Callback Function
def callback(indata, outdata, frames, time, status):


This function is executed continuously by sounddevice for each audio block.

Step-by-step inside the callback:

Check running state

if not running:
    outdata[:] = 0
    return


If stopped, output silence.

Extract mono input

audio = indata[:, 0]


Apply noise reduction (optional)

audio = nr.reduce_noise(
    y=audio,
    sr=SAMPLE_RATE,
    stationary=True,
    prop_decrease=0.8
)


Assumes stationary noise

Reduces noise by approximately 80%

Apply gain

audio *= gain_value


Prevent clipping

audio = np.clip(audio, -1.0, 1.0)


Send audio to output

outdata[:, 0] = audio

Stream Management
with sd.Stream(...):
    while running:
        sd.sleep(100)


Opens a full-duplex audio stream

Keeps the stream alive while running is True

Uses a sleep loop instead of blocking the GUI thread

5. Threaded Start/Stop Control
def start_audio():
    running = True
    threading.Thread(target=audio_loop, daemon=True).start()


Starts audio processing in a daemon thread

Prevents the GUI from freezing

def stop_audio():
    running = False


Stops audio by signaling the callback to output silence

6. Real-Time Control Handlers
Gain Adjustment
def update_gain(val):
    gain_value = float(val)


Called automatically when the slider moves

Gain changes take effect immediately

Noise Reduction Toggle
def toggle_noise():
    noise_reduction_enabled = noise_var.get()


Reads checkbox state

Enables or disables DSP noise suppression

Device Selection
def set_input_device(event):
    input_device = input_devices[input_combo.current()]

def set_output_device(event):
    output_device = output_devices[output_combo.current()]


Updates selected input/output device indices

Takes effect the next time audio starts

7. Audio Device Enumeration
devices = sd.query_devices()


Retrieves all system audio devices

if d['max_input_channels'] > 0:


Filters microphones

if d['max_output_channels'] > 0:


Filters speakers/headphones

Two lists are created:

Device indices (used by sounddevice)

Device names (shown in the GUI)

8. GUI Construction (Tkinter)
Main Window
root = tk.Tk()
root.title("Professional Sound Amplifier")
root.geometry("420x380")


Fixed-size application window

Input / Output Selection
ttk.Combobox(..., values=input_names)


Dropdown menus populated with detected devices

Selection events update internal device state

Gain Slider
ttk.Scale(from_=1.0, to=10.0)


Real-time amplification control

Default gain = 2×

Max gain = 10×

Noise Reduction Checkbox
ttk.Checkbutton(variable=noise_var)


Toggles DSP noise cancellation

Start / Stop Buttons
ttk.Button(command=start_audio)
ttk.Button(command=stop_audio)


Starts and stops the real-time audio stream

9. Event Loop
root.mainloop()


Runs the GUI event dispatcher

Keeps the application alive

10. Overall Behavior Summary

This application functions as:

A real-time microphone-to-speaker amplifier

With optional noise suppression

Adjustable gain

Selectable input/output devices

Low-latency streaming via callback-based DSP

Thread-safe GUI interaction

The architecture cleanly separates:

Audio processing (real-time, threaded)

UI control (main thread)

Device abstraction (sounddevice)
