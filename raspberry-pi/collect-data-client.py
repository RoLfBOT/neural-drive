import io
import sys
import socket
import time
import cv2
import numpy as np
import threading
import struct
import picamera
import serial

class ControlClient(object):
    def __init__(self, host, port, serial_port):
        self.host = host
        self.port = port
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        self.controls = {
            'forward': 'f255',
            'backward': 'b255',
            'right': 'r255',
            'left': 'l255'
        }

    def get_control(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))

        print("connection established control")

        while True:
            
            msg = self.socket.recv(1024).decode('utf-8')
            if msg == "quit":
                break
            self.ser.write(self.controls[msg].encode())

        self.socket.close()

class StreamClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_stream(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        self.connection = self.socket.makefile('wb')

        print("established connection")

        try:
            output = SplitFrames(self.connection)
            with picamera.PiCamera(resolution='640x480', framerate=15) as camera:   
                time.sleep(2)

                start = time.time()
                camera.start_recording(output, format='mjpeg')
                camera.wait_recording(10000000)
                camera.stop_recording()

                self.connection.write(struct.pack('<L', 0))

        finally:
            self.connection.close()
            self.socket.close()
            finish = time.time()
            print('Sent %d images in %d seconds at %.2ffps' % (output.count, finish-start, output.count / (finish-start)))

class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

if __name__ == "__main__":
    host, port1, port2 = '192.168.137.1', 6678, 6679
    serial_port = '/dev/ttyACM0'

    stc = StreamClient(host, port1)
    ctc = ControlClient(host, port2, serial_port)

    stream_process = threading.Thread(target=stc.send_stream)
    # control_process = threading.Thread(target=ctc.get_control)
    stream_process.daemon = True
    
    # control_process.start()
    stream_process.start()
    ctc.get_control()