import pygame
import threading
import time
from server import GameServer
from game import Game

class OrbitPongLauncher:
    def __init__(self):
        self.server = None
        self.game = None
        
    def start_game(self):
        time.sleep(0.5)  # Kurz warten bis Server gestartet ist
        pygame.init()
        
        self.game = Game()
        if self.server:
            self.game.server = self.server
            self.server.game = self.game
        
        try:
            self.game.run()
        finally:
            pass 
    
    def run(self, host='0.0.0.0', port=12345):
        self.server = GameServer(host, port)
        
        # Server start() in eigenem Thread
        server_setup_thread = threading.Thread(target=self.server.setup, daemon=True)
        server_setup_thread.start()
        
        # Server update() in eigenem Thread  
        server_loop_thread = threading.Thread(target=self.server.loop, daemon=True)
        server_loop_thread.start()
        
        # Game im Main Thread starten (für pygame)
        self.start_game()

if __name__ == "__main__":
    host = input("Server IP (0.0.0.0): ").strip() or '0.0.0.0'
    port = int(input("Port (12345): ").strip() or '12345')
    
    launcher = OrbitPongLauncher()
    launcher.run(host, port)