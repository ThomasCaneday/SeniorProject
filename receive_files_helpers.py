import socket, struct, os, time, csv
from datetime import datetime

def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def connect_socket(HOST, PORT, s):
    s.connect((HOST, PORT))
