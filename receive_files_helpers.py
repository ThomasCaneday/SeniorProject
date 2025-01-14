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
