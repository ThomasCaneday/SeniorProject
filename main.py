from record import record
from daq_wav_to_csv import convert_wav_to_csv
from server import send_files, establish_connection

# Return boolean value if connection is established, and return client_socket object to connect to.
tf, clisock = establish_connection()

# Run continuous loop that records 60 seconds of audio, then sends the WAV files, converted
# to CSVs, to the client socket.
try:
    while tf:
        record()
        convert_wav_to_csv('recorded_audio.wav')
        send_files(clisock)
except KeyboardInterrupt:
    # NOTICE: Two while loops need to be interrupted when manually stopping the
    # program (one recording and the one in this try scope).
    print("Keyboard interrupted in main!")