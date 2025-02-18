import numpy as np
import matplotlib.pyplot as plt
import wave
import sys
from scipy.fftpack import fft, fftfreq

def load_audio(file_path):
    """Load audio data from a WAV file"""
    with wave.open(file_path, 'rb') as wf:
        sample_rate = wf.getframerate()
        num_samples = wf.getnframes()
        audio_data = np.frombuffer(wf.readframes(num_samples), dtype=np.int16)
    return audio_data, sample_rate

def plot_signal(audio, sample_rate, title):
    """Plot the frequency spectrum, only showing 0-150 Hz"""
    N = len(audio)
    yf = np.abs(fft(audio))  # Compute magnitude of FFT
    xf = fftfreq(N, 1 / sample_rate)  # Frequency axis

    # Keep only frequencies from 0 to 150 Hz
    mask = (xf >= 0) & (xf <= 150)
    xf = xf[mask]
    yf = yf[mask]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(xf, yf)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()


# Check command-line arguments
if len(sys.argv) < 3 or sys.argv[2] not in ["spectrum", "spectrogram"]:
    print("Usage: python test_visualization.py --type [spectrum|spectrogram]")
    sys.exit(1)

# Load raw and filtered audio
raw_audio, HIGH_RATE = load_audio("recordings/raw_audio.wav")
filtered_audio, TARGET_RATE = load_audio("filtered_audio.wav")

# Handle spectrum visualization
if sys.argv[2] == "spectrum":
    plot_signal(raw_audio, HIGH_RATE, "Original Signal Spectrum")
    plot_signal(filtered_audio, TARGET_RATE, "Filtered Signal Spectrum")
