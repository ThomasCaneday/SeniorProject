import wave
import pyaudio

# Configuration
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of audio channels (mono)
RATE = 44100  # Sample rate (Hz)

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

print("Recording... Press Ctrl+C to stop.")

frames = []

try:
    # Continuously record audio
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

except KeyboardInterrupt:
    print("\nRecording stopped.")

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
