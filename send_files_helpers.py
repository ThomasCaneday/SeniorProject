import os, time, struct

def get_file_size(file_name):
    file_size = os.path.getsize(file_name)
    return file_size
