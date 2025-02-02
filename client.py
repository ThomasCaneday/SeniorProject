from receive_files_helpers import get_socket, connect_socket, create_dir, get_metadata_length_bytes, get_metadata_length, get_metadata_bytes, get_metadata, get_fname_fsize_sent_time, update_received_data, write_file, get_time, calculate_latency, process_received_file

# Run this file on the receiving node

# Client setup
HOST = "127.0.0.1" # Change IP to respective address
PORT = 5001

s = get_socket()
connect_socket(HOST, PORT, s)

# Directory to save received files
SAVE_DIR = "received_files"
create_dir(SAVE_DIR)

# Metrics
latencies = []
data_rates = []

# Latency and Data Rate Files
LATENCY_LOG_FILE = "latency_counts.csv"
DATA_RATE_LOG_FILE = "data_rate_counts.csv"


def receive_files():
    # TODO: Check if total_data_received should be globally accessible
    global total_data_received

    while True:
        try:
            # Receive metadata length
            metadata_length_bytes = get_metadata_length_bytes(s)
            metadata_length = get_metadata_length(metadata_length_bytes)

            # Receive metadata
            metadata_bytes = get_metadata_bytes(s, metadata_length)
            metadata = get_metadata(metadata_bytes)

            try:
                file_name, file_size, sent_time = get_fname_fsize_sent_time(metadata)
                file_size = int(file_size)
                sent_time = float(sent_time)
            except ValueError:
                raise ValueError(f"Malformed metadata: {metadata}")
            
            # Receive file content
            received_data = b""
            received_data = update_received_data(s, file_size, received_data)
            
            # Save the file
            write_file(SAVE_DIR, file_name, received_data)
            
            process_received_file(file_name, received_data, sent_time, LATENCY_LOG_FILE, latencies, DATA_RATE_LOG_FILE, data_rates)
        except Exception as e:
            print(f"Error receiving file: {e}")

# Start receiving files
receive_files()
