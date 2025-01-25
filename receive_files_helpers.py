import socket, struct, os, time, csv
from datetime import datetime

def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def connect_socket(HOST, PORT, s):
    s.connect((HOST, PORT))

def create_dir(dir):
    os.makedirs(dir, exist_ok=True)

def get_metadata_length(metadata_length_bytes):
    if not metadata_length_bytes:
        raise ValueError("Failed to receive metadata length.")
    metadata_length = struct.unpack(">I", metadata_length_bytes)[0]
    return metadata_length

def get_metadata_length_bytes(s):
    metadata_length_bytes = s.recv(4)
    return metadata_length_bytes

def get_metadata_bytes(s, metadata_length):
    metadata_bytes = s.recv(metadata_length)
    return metadata_bytes

def get_metadata(metadata_bytes):
    if not metadata_bytes:
        raise ValueError("Failed to receive metadata.")
    metadata = metadata_bytes.decode()
    return metadata

def get_fname_fsize_sent_time(metadata):
    file_name, file_size, sent_time = metadata.split(",")
    return file_name,file_size,sent_time

def get_chunk(s, file_size, received_data):
    chunk = s.recv(min(1024, file_size - len(received_data)))
    return chunk

def update_received_data(s, file_size, received_data):
    while len(received_data) < file_size:
        chunk = get_chunk(s, file_size, received_data)
        if not chunk:
            # error_count += 1
            raise ValueError("Incomplete file data received.")
        received_data += chunk
    return received_data

def write_file(dir, file_name, received_data):
    file_path = get_file_path(dir, file_name)
    with open(file_path, 'wb') as f:
        f.write(received_data)

def get_file_path(SAVE_DIR, file_name):
    file_path = os.path.join(SAVE_DIR, file_name)
    return file_path

def get_time():
    t = time.time()
    return t

def calculate_latency(received, sent):
    l = received - sent
    return l

def log_data_rate(file_name, total_data_received, start_time, end_time, DATA_RATE_LOG_FILE, data_rates):
    # Calculate and log the data rate to a CSV file.
    try:
        elapsed_time = end_time - start_time
        data_rate = total_data_received / elapsed_time if elapsed_time > 0 else 0
        data_rates.append(data_rate)
        
        with open(DATA_RATE_LOG_FILE, mode="a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            # Write header if file is empty
            if csv_file.tell() == 0:
                writer.writerow(["Timestamp", "File Name", "Data Rate (bytes/second)"])
            
            # Write data rate
            writer.writerow([datetime.now(), file_name, data_rate])
        
        print(f"Data rate for {file_name}: {data_rate:.2f} bytes/second logged.")
    except Exception as e:
        print(f"Failed to log data rate for {file_name}: {e}")
