import socket
import time
import picamera
import serial
from random import randint, random

with picamera.PiCamera() as camera:
       
    camera.resolution = (640, 480)
    camera.framerate = 24

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('wb')
    # Connection to the arduino
    ser = serial.Serial('/dev/serial/by-path/platform-bcm2708_usb-usb-0:1.4:1.0', 9600)
    
    def sendDriveCmd( speed, curvature ):
        s = str(speed) + ',' + str(curvature) + ';'
        ser.write(s);
        print s
        return
    
    try:
        #main loop
        while 1:
            camera.start_recording(connection, format='h264')
            camera.wait_recording(5)
            camera.stop_recording()
            #random commands for the motor
            sendDriveCmd(randint(0,100), random())           
            
    finally:
        connection.close()
        server_socket.close()

    