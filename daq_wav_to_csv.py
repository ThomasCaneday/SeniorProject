import numpy as np
import scipy.io.wavfile as wav
import csv
import datetime

def extract_wav_to_csv(file_path):
    # Read the WAV file
    sample_rate, data = wav.read(file_path)
    
    # Here we assume mono channel for simplicity, you can adjust for stereo
    acoustic_data = data if len(data.shape) == 1 else data[:, 0]

    # Create timestamps (assuming a continuous sampling rate)
    timestamps = np.arange(0, len(acoustic_data) / sample_rate, 1 / sample_rate)

    return sample_rate, timestamps, acoustic_data

def write_daq_csv(sample_rate, start_time, acoustic_data, timestamps, file_name='test_daq.csv'):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the first row: {sample rate, POSIX timestamp of start, flag}
        writer.writerow([sample_rate, start_time, '1']) # Assume 1 flag is a placeholder

        # Write the subsequent rows: {time, acoustic measurement value}
        for t, measurement in zip(timestamps, acoustic_data):
            writer.writerow([t, measurement])

def convert_wav_to_csv(wav_file='data.wav'):
    wav_file_path = wav_file
    sample_rate, timestamps, acoustic_data = extract_wav_to_csv(wav_file_path)

    # Start time (POSIX timestamp at start of recording, assuming it's the time of WAV file creation)
    start_time = int(datetime.datetime.now().timestamp())

    # Write the CSVs
    write_daq_csv(sample_rate, start_time, acoustic_data, timestamps)
    print("Wav file converted to CSV.")
