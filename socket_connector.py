"""
DO NOT EDIT ANY LINE IN THIS FILE
However, it is important to read and understand the code below as you will be calling functions from this file

"""

import requests 
import socket

class PanelConnector():
    def __init__(self, simulator = True):
        if simulator:
            self.panel_ip = 'localhost'
            self.panel_port = 16021
            self.stream_port = 16021
            self.auth_token = 'simulator'
        else:
            # These lines of code are needed to connect to the actual Nanoleaf panels
            # You may need to generate a new auth_token for this to work.  See the detailed
            # instructions in the Nanoleaf API
            self.panel_ip = '192.168.2.1'
            self.panel_port = 16021
            self.stream_port = 60221
            self.auth_token = "2uv0tUmzfvHgMS5vBBKp2JDcLq7UPIoS"
            data = {"write" : {"command" : "display", "animType" : "extControl"}}
            r = requests.put(url = "http://" + str(self.panel_ip) + ":" + str(self.panel_port) + \
                             "/api/v1/" + self.auth_token + "/effects" , data = json.dumps(data))
            
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
       
    
    def get_panel_layout(self):
        """Gets panel layout"""
        
        return requests.get(url = "http://" + str(self.panel_ip) + ":" + str(self.panel_port) + "/api/v1/" + self.auth_token + "/panelLayout")
    
    
    def send_data_to_panels(self, list_of_bytes):
        """Sends data to panels"""
        
        return self.sock.sendto(bytes(list_of_bytes), (self.panel_ip, self.stream_port))