import wave
import pyaudio
import time

def record():
    CHUNK = 1024  # Number of audio frames per buffer
    FORMAT = pyaudio.paInt16  # Audio format
    CHANNELS = 1  # Number of audio channels (mono)
    # RATE = 44100   Sample rate (Hz)
    RATE = 300 # Sample rate (Hz) for frequency of 150 Hz

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

    # Save audio to a WAV file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {OUTPUT_FILENAME}")

