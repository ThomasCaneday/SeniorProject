import os, time, struct

def get_file_size(file_name):
    file_size = os.path.getsize(file_name)
    return file_size

def get_metadata(file_name, file_size):
    metadata = f"{file_name},{file_size},{time.time()}"
    return metadata

def get_metadata_bytes(file_name):
    file_size = get_file_size(file_name)
    metadata = get_metadata(file_name, file_size)
    metadata_bytes = metadata.encode()
    return metadata_bytes

def send_metadata_and_length(client_socket, metadata_bytes):
    client_socket.sendall(struct.pack(">I", len(metadata_bytes))) # 4-byte length prefix
    client_socket.sendall(metadata_bytes)

def send_file_chunks(client_socket, file_name):
    with open(file_name, 'rb') as f:
        while chunk := f.read(1024):
                        # data = f.read()
            client_socket.sendall(chunk)

def increment_error_count(file_name, error_counts):
    # Increment the error count for a given file and log the error.
    if file_name in error_counts:
        error_counts[file_name] += 1
    else:
        error_counts[file_name] = 1
    print(f"Error count for {file_name}: {error_counts[file_name]}")

def write_error_counts_to_csv(file_path, error_counts):
    # Write the current error counts to a CSV file.
    try:
        with open(file_path, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            # Write header
            writer.writerow(["File Name", "Error Count"])
            # Write error counts
            for file_name, count in error_counts.items():
                writer.writerow([file_name, count])
        print(f"Error counts written to {file_path}")
    except Exception as e:
        print(f"Failed to write error counts to CSV: {e}")
        traceback.print_exc()
