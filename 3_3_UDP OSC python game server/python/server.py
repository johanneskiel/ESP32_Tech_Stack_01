from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import time



class Client:
    def __init__(self, name, color, ip):
        self.udp = udp_client.SimpleUDPClient(ip, 8888)
        self.last_activity = time.time()
        self.name = name
        self.color = color
        self.ip = ip
        self.player = None



class GameServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.game = None
        self.server = None
        self.disconnect_timeout = 1.0
        self.running = False
        

    def setup(self):
        disp = dispatcher.Dispatcher()
        disp.map("/connect", self.connect_handler, needs_reply_address=True)
        disp.map("/poti", self.poti_handler, needs_reply_address=True)
        
        self.server = osc_server.ThreadingOSCUDPServer((self.host, self.port), disp)
        self.running = True
        print(f"Server started on {self.host}:{self.port}")
        self.server.serve_forever()


    def loop(self):
        while self.running:
            self.check_connections()
            time.sleep(.5)
    

    def check_connections(self):
        current_time = time.time()
        
        for client in self.clients[:]:
            if current_time - client.last_activity > self.disconnect_timeout:
                print(f"Player {client.name} disconnected (timeout)")
                self.game.remove_network_player(client.player)
                self.clients.remove(client)
    

    def connect_handler(self, client_address, server_address, name, color_str):
        ip = client_address[0]
        color = tuple(map(int, color_str.split()))
        
        existing_client = None
        for client in self.clients:
            if client.ip == ip:
                existing_client = client
                break
    
        if not existing_client:
            client = Client(name, color, ip)
            self.clients.append(client)
            client.player = self.game.add_network_player(name, color)
            print(f"Player {name} connected from {ip} with color {color}")


    def poti_handler(self, client_address, server_address, poti_value):
        ip = client_address[0]
        for client in self.clients:
            if client.ip == ip:
                poti_value = float(poti_value)
                client.last_activity = time.time()
                client.player.set_target_position_float(poti_value)


    def send_led_blink(self, player):
        for client in self.clients:
            if client.player == player:
                client.udp.send_message("/led_blink", True)
                break
    




    
    