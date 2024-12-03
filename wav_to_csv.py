import wave
import csv
import struct
import sys

def wav_to_csv(wav_file_path, csv_file_path='data.csv'):
    try:
        # Open the WAV file
        with wave.open(wav_file_path, 'rb') as wav_file:
            # Extract WAV file properties
            n_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            n_frames = wav_file.getnframes()

            print(f"Channels: {n_channels}, Sample Width: {sample_width}, Frame Rate: {frame_rate}, Frames: {n_frames}")

            # Read frames from the WAV file
            frames = wav_file.readframes(n_frames)

            # Determine the format for unpacking based on sample width
            if sample_width == 1:  # 8-bit audio
                fmt = f'{n_frames * n_channels}B'
            elif sample_width == 2:  # 16-bit audio
                fmt = f'{n_frames * n_channels}h'
            else:
                print("Unsupported sample width")
                return

            # Unpack frames into a list of integers
            samples = struct.unpack(fmt, frames)

        # Write the samples to a CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write header
            header = ['Sample Index'] + [f'Channel {i + 1}' for i in range(n_channels)]
            csv_writer.writerow(header)

            # Write each sample to the CSV file
            for i in range(0, len(samples), n_channels):
                row = [i // n_channels] + list(samples[i:i + n_channels])
                csv_writer.writerow(row)

        print(f"WAV data successfully written to {csv_file_path}")

    except FileNotFoundError:
        print("File not found. Please provide a valid WAV file path.")
    except wave.Error as e:
        print(f"Error reading WAV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
