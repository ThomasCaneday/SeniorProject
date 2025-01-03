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
