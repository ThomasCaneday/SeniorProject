import wave
import pyaudio
import time
import numpy as np
import scipy.signal as signal

def record():
    CHUNK = 1024  # Number of audio frames per buffer
    FORMAT = pyaudio.paInt16  # Audio format
    CHANNELS = 1  # Number of audio channels (mono)
    RATE = 8000   # Sample rate (Hz)
    TARGET_RATE = 300 # Sample rate (Hz) for frequency of 150 Hz

    # Output file
    OUTPUT_FILENAME = "recorded_audio.wav"

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("Recording for 60 seconds... Press Ctrl+C to stop.")

    frames = []

    # Initialize start_time for determining recording time (difference)
    start_time = time.time()

    try:
        # Continuously record audio
        while time.time() - start_time < 60:  # Stop after 60 seconds
            data = stream.read(CHUNK)
            frames.append(data)

    except KeyboardInterrupt:
        print("\nRecording stopped manually.")

    print("\nRecording stopped automatically after 60 seconds.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert raw audio to NumPy array
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

    # Apply a low-pass filter (cutoff at 20 Hz)
    cutoff_freq = 20  # Hz
    nyquist = RATE / 2
    b, a = signal.butter(4, cutoff_freq / nyquist, btype='low')
    filtered_audio = signal.filtfilt(b, a, audio_data)

    # Downsample the filtered signal to 300 Hz
    num_samples_target = int(len(filtered_audio) * (TARGET_RATE / RATE))
    downsampled_audio = signal.resample(filtered_audio, num_samples_target).astype(np.int16)

    # Save audio to a WAV file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {OUTPUT_FILENAME}")

