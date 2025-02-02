import traceback
from send_files_helpers import get_metadata_bytes, send_metadata_and_length, send_file_chunks, increment_error_count, write_error_counts_to_csv
# Reusing boilerplate get_socket helper function from receive_files section
from receive_files_helpers import get_socket

# Server setup (boilerplate)
HOST = ''  # Bind to all interfaces
PORT = 5001
s = get_socket()
s.bind((HOST, PORT))
s.listen(5)
print('Server is now running.')

# Files to send
daq_file = "test_daq.csv" # Change this if testing sending the file

# TODO: Delete or account for IMU and GPS files
# imu_file = "original_imu.csv"
# gps_file = "original_gps.csv"
# CSV_FILES = [daq_file, imu_file, gps_file]
CSV_FILES = [daq_file] # If DAQ file is the only necessary file

# Initialize a dictionary to track error counts for each file transmission
error_counts = {file_name: 0 for file_name in CSV_FILES}
ERROR_LOG_FILE = "test_error_counts.csv"  # Name of the CSV file to store error counts

def send_files(client_socket):
    for file_name in CSV_FILES:
        try:
            # Get metadata from file name and size, then encode it into bytes
            metadata_bytes = get_metadata_bytes(file_name)

            # Send metadata length and metadata
            send_metadata_and_length(client_socket, metadata_bytes)
            
            # Send file content
            send_file_chunks(client_socket, file_name)
            
            print(f"Sent {file_name} to client.")
        except Exception as e:
            print(f"Error sending {file_name}: {e}")
            traceback.print_exc()
            increment_error_count(file_name, error_counts)
    write_error_counts_to_csv(ERROR_LOG_FILE, error_counts)  # Save error counts to CSV

def establish_connection():
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established.")
    return True, client_socket
