import socket

class socket_handler:
    def __init__(self, HOST, PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        self.sock = self.sock.accept()[0]

    def send_message(self, message):
        self.sock.send(message.encode())

    def recive_message(self):
        return self.sock.recv(1024).decode()
        
class cube_robot:
    def __init__(self):
        IP = "xxx.xxx.xxx.xxx"
        FIRST_PORT = 5001
        SECOND_PORT = 5000
        print("start_first_connect")
        self.first_ev3_socket = socket_handler(IP, FIRST_PORT)
        print("first_connect")

        print("start_second_connect")
        self.second_ev3_socket = socket_handler(IP, SECOND_PORT)
        print("second_connect")

    def check_side(self, rotation):
        for side in ["U", "F", "R"]:
            if side in rotation:
                return True
        return False

    def rotate(self, rotation):
        if isinstance(rotation, list):
            for spin in rotation:
                if self.check_side(spin):
                    self.first_ev3_socket.send_message(spin)
                else:
                    self.second_ev3_socket.send_message(spin)
            self.second_ev3_socket.recive_message()
            self.first_ev3_socket.recive_message()
        else:
            if self.check_side(rotation):
                self.first_ev3_socket.send_message(rotation)
                self.first_ev3_socket.recive_message()
            else:
                self.second_ev3_socket.send_message(rotation)
                self.second_ev3_socket.recive_message()
