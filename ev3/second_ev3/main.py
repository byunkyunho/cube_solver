#!/usr/bin/env python3

import time
import socket
import re
from ev3dev.ev3 import *

class socket_handler:
    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def send_message(self, message):
        self.s.send(message.encode())

    def recive_message(self):
        return self.s.recv(1024).decode()   

MOTOR_SPEED = 1000
WHITE_MOTOR = MediumMotor("outB")
ORANGE_MOTOR = LargeMotor("outC")
BLUE_MOTOR = LargeMotor("outD")

IP = "192.168.1.8"
PORT = 5000


while True:
    try:
        main_socket = socket_handler(IP, PORT)
        break   
    except :
        pass

motor_list = {"D":WHITE_MOTOR,"L":BLUE_MOTOR,  "B":ORANGE_MOTOR}

while True:
    response = main_socket.recive_message()

    face = "".join(re.findall("[A-Z]", response))

    spin =   (180 if "'" in response else -180) if "2" in response else   (90 if "'" in response else -90)

    motor_list[face].run_to_rel_pos(position_sp=spin, speed_sp=MOTOR_SPEED, stop_action="hold")
    
    main_socket.send_message("done")    