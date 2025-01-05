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
