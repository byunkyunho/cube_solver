#!/usr/bin/env python3

from ev3dev.ev3 import *
import time 
import socket
import re 

GREEN_MOTOR = LargeMotor("outD")
RED_MOTOR = LargeMotor("outC")
YELLOW_MOTOR = MediumMotor("outB")

class socket_handler:
    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def send_message(self, message):
        self.s.send(message.encode())

    def recive_message(self):
        return self.s.recv(1024).decode()

IP = "192.168.1.8" #놑북
PORT = 5001
while True:
    try:
        main_socket = socket_handler(IP, PORT)
        break
    except :
        pass

motor_list = {"U":YELLOW_MOTOR, "R":GREEN_MOTOR, "F":RED_MOTOR}

MOTOR_SPEED = 1000
while True:
    response = main_socket.recive_message()

    face = "".join(re.findall("[A-Z]", response))

    spin =  (180 if "'" in response else -180) if "2" in response else   (90 if "'" in response else -90)

    motor_list[face].run_to_rel_pos(position_sp=spin, speed_sp=MOTOR_SPEED, stop_action="hold")
    
    main_socket.send_message("done")    