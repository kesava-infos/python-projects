import sounddevice as sd
import numpy as np
import noisereduce as nr
import threading
import tkinter as tk
from tkinter import ttk

# ---------------- AUDIO CONFIG ----------------
CHANNELS = 1
BLOCK_SIZE = 1024

# sd.default.hostapi = 'pulse'  # safer on Linux

# ---------------- GLOBAL STATE ----------------
running = False
gain_value = 2.0
noise_reduction_enabled = True
stream = None

input_device = None
output_device = None
SAMPLE_RATE = None


# ---------------- AUDIO PROCESSING ----------------
def audio_loop():
    global stream, SAMPLE_RATE

    device_info = sd.query_devices(input_device)
    SAMPLE_RATE = int(device_info['default_samplerate'])

    def callback(indata, outdata, frames, time, status):
        if not running:
            outdata[:] = 0
            return

        audio = indata[:, 0]

        if noise_reduction_enabled:
            audio = nr.reduce_noise(
                y=audio,
                sr=SAMPLE_RATE,
                stationary=True,
                prop_decrease=0.8
            )

        audio *= gain_value
        audio = np.clip(audio, -1.0, 1.0)

        outdata[:, 0] = audio

    try:
        with sd.Stream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            device=(input_device, output_device),
            channels=CHANNELS,
            dtype='float32',
            callback=callback
        ):
            while running:
                sd.sleep(100)
    except Exception as e:
        print("Audio error:", e)
        stop_audio()


# ---------------- GUI CONTROL ----------------
def start_audio():
    global running
    if running:
        return
    running = True
    threading.Thread(target=audio_loop, daemon=True).start()


def stop_audio():
    global running
    running = False


def update_gain(val):
    global gain_value
    gain_value = float(val)


def toggle_noise():
    global noise_reduction_enabled
    noise_reduction_enabled = noise_var.get()


def set_input_device(event):
    global input_device
    input_device = input_devices[input_combo.current()]


def set_output_device(event):
    global output_device
    output_device = output_devices[output_combo.current()]


# ---------------- DEVICE ENUMERATION ----------------
devices = sd.query_devices()

input_devices, input_names = [], []
output_devices, output_names = [], []

for i, d in enumerate(devices):
    if d['max_input_channels'] > 0:
        input_devices.append(i)
        input_names.append(d['name'])
    if d['max_output_channels'] > 0:
        output_devices.append(i)
        output_names.append(d['name'])

input_device = input_devices[0]
output_device = output_devices[0]

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Professional Sound Amplifier")
root.geometry("420x380")
root.resizable(False, False)

ttk.Label(root, text="🎧 Sound Amplifier", font=("Arial", 16, "bold")).pack(pady=10)

# Input Device
ttk.Label(root, text="Input Microphone").pack()
input_combo = ttk.Combobox(root, values=input_names, state="readonly")
input_combo.pack(pady=5)
input_combo.bind("<<ComboboxSelected>>", set_input_device)
input_combo.current(0)

# Output Device
ttk.Label(root, text="Output Speaker / Headphones").pack()
output_combo = ttk.Combobox(root, values=output_names, state="readonly")
output_combo.pack(pady=5)
output_combo.bind("<<ComboboxSelected>>", set_output_device)
output_combo.current(0)

# Gain Slider
ttk.Label(root, text="Amplification Level").pack(pady=10)
gain_slider = ttk.Scale(
    root, from_=1.0, to=10.0,
    orient="horizontal",
    command=update_gain
)
gain_slider.set(gain_value)
gain_slider.pack(fill="x", padx=20)

# Noise Reduction
noise_var = tk.BooleanVar(value=True)
ttk.Checkbutton(
    root,
    text="Enable Noise Cancellation",
    variable=noise_var,
    command=toggle_noise
).pack(pady=10)

# Buttons
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=20)

ttk.Button(btn_frame, text="▶ Start", width=12, command=start_audio).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="⏹ Stop", width=12, command=stop_audio).grid(row=0, column=1, padx=10)

# Footer
ttk.Label(root, text="Low latency • Real-time DSP", font=("Arial", 9)).pack(pady=5)

root.mainloop()
