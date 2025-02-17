import numpy as np
import scipy.signal as signal
import wave
import pyaudio
import time

def record():
    CHUNK = 1024  
    FORMAT = pyaudio.paInt16  
    CHANNELS = 1  
    HIGH_RATE = 8000  # Original sample rate
    TARGET_RATE = 300  # Final downsampled rate

    RAW_OUTPUT_FILENAME = "recordings/raw_audio.wav"
    FILTERED_OUTPUT_FILENAME = "filtered_audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=HIGH_RATE,  
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording for 60 seconds... Press Ctrl+C to stop.")

    frames = []
    start_time = time.time()

    try:
        while time.time() - start_time < 60:  
            data = stream.read(CHUNK)
            frames.append(data)

    except KeyboardInterrupt:
        print("\nRecording stopped manually.")

    print("\nRecording stopped automatically after 60 seconds.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert raw audio to NumPy array
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

    ### **Save Raw Audio Before Filtering** ###
    with wave.open(RAW_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(HIGH_RATE)
        wf.writeframes(audio_data.tobytes())

    print(f"Raw audio saved as {RAW_OUTPUT_FILENAME}")

    # Apply Low-Pass Filter (cutoff at 20 Hz)
    cutoff_freq = 20  # Hz
    nyquist = HIGH_RATE / 2
    b, a = signal.butter(4, cutoff_freq / nyquist, btype='low')
    filtered_audio = signal.filtfilt(b, a, audio_data)

    # Downsample the filtered signal to 300 Hz
    num_samples_target = int(len(filtered_audio) * (TARGET_RATE / HIGH_RATE))
    downsampled_audio = signal.resample(filtered_audio, num_samples_target).astype(np.int16)

    # Save the processed audio
    with wave.open(FILTERED_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(TARGET_RATE)
        wf.writeframes(downsampled_audio.tobytes())

    print(f"Filtered and downsampled audio saved as {FILTERED_OUTPUT_FILENAME}")

record()