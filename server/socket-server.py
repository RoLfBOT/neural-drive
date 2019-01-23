import io
import os
import socket
import struct
import cv2
import numpy as np
from PIL import Image

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 6678))
server_socket.listen(0)

connection = server_socket.accept()[0].makefile('rb')
print('connection accepted')

try:
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        image_stream.seek(0)
        image = Image.open(image_stream)

        print('Image is %dx%d' % image.size)
        cv2.imshow('Pi', cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB))
        cv2.waitKey(1)

finally:
    connection.close()
    server_socket.close()
