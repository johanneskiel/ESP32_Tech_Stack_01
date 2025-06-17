import pygame
import random
import math
import sys
from player import Player
from item import Ball, PowerUp, PowerDown

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORBIT_COLOR = (130, 130, 130)
BASE_ORBIT_DISTANCE = 150
ORBIT_SPACING = 50
MAX_ORBIT_RADIUS = 400
ITEM_FADEOUT_RADIUS = 100

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Orbit Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.score = 0
        self.chain_hits = 0
        self.chain_players = set()
        self.chain_flash_timer = 0
        self.chain_flash_color = None
        self.flash_items = []
        self.players = []
        self.orbit_slots = [None] * 10
        self.ball = None
        self.items = []
        self.server = None
        
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.spawn_ball()
    
    def reset_chain(self):
        self.chain_hits = 0
        self.chain_players.clear()
        
    def flash_chain_bar(self, color):
        from item import PowerUp, PowerDown
        
        bar_center_x = 120  # Mitte der Progress Bar (20 + 200/2)
        bar_y = 80  # Progress Bar Y Position + 10
        
        for i in range(8):
            if color == (255, 100, 100):
                flash_item = PowerDown(bar_center_x + i * 10 - 35, bar_y + i * 3 - 12)
            else:
                flash_item = PowerUp(bar_center_x + i * 10 - 35, bar_y + i * 3 - 12)
            
            flash_item.collision_triggered = True
            flash_item.growth_timer = 20 + i * 2
            flash_item.fade_timer = 30 + i * 3
            
            import random
            flash_item.vel_x = random.uniform(-3, 3)
            flash_item.vel_y = random.uniform(-3, 3)
            
            self.flash_items.append(flash_item)
    
    def add_network_player(self, name="Remote Player", color=(100, 100, 255)):
        slot_index = None
        for i in range(len(self.orbit_slots) - 1, -1, -1):
            if self.orbit_slots[i] is None:
                orbit_distance = BASE_ORBIT_DISTANCE + i * ORBIT_SPACING
                if orbit_distance <= MAX_ORBIT_RADIUS:
                    slot_index = i
                    break
        
        if slot_index is None:
            return None
        
        orbit_distance = BASE_ORBIT_DISTANCE + slot_index * ORBIT_SPACING
        player = Player(slot_index, orbit_distance)
        player.center_x = self.center_x
        player.center_y = self.center_y
        player.set_name_and_color(name, color)
        player.update_position()
        
        self.orbit_slots[slot_index] = player
        self.players.append(player)
        return player
    
    def remove_network_player(self, player):
        if player in self.players:
            self.players.remove(player)
            self.orbit_slots[player.id] = None

    def spawn_ball(self):
        if self.ball is not None and self.chain_hits > 0:
            self.flash_chain_bar((255, 100, 100))
        self.ball = Ball(self.center_x, self.center_y)
        self.reset_chain()
    
    def spawn_item(self):
        if random.random() < 0.005:
            item_type = random.choice(['powerup', 'powerdown'])
            if item_type == 'powerup':
                item = PowerUp(self.center_x, self.center_y)
            else:
                item = PowerDown(self.center_x, self.center_y)
            self.items.append(item)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        for flash_item in self.flash_items[:]:
            flash_item.update()
            if hasattr(flash_item, 'remove_me') and flash_item.remove_me:
                self.flash_items.remove(flash_item)
        
        for player in self.players:
            player.update(keys, self.center_x, self.center_y)
        
        if self.ball:
            self.ball.update()
            
            for player in self.players:
                if self.ball.check_collision_with_player(player):
                    if self.ball.handle_collision(player):
                        if player.id not in self.chain_players:
                            self.chain_players.add(player.id)
                            self.chain_hits += 1
                            
                            if len(self.chain_players) == len(self.players):
                                self.score += self.chain_hits
                                self.flash_chain_bar((100, 150, 255))
                                self.reset_chain()
                        
                        if self.server:
                            self.server.send_led_blink(player)
                        break
        
        if self.ball:
            distance_from_center = math.sqrt((self.ball.x - self.center_x)**2 + (self.ball.y - self.center_y)**2)
            max_orbit_radius = self.get_max_orbit_radius()
            
            if distance_from_center > max_orbit_radius + ITEM_FADEOUT_RADIUS:
                fade_progress = (distance_from_center - (max_orbit_radius + ITEM_FADEOUT_RADIUS)) / ITEM_FADEOUT_RADIUS
                fade_progress = min(1.0, max(0.0, fade_progress))
                self.ball.alpha = int(255 * (1.0 - fade_progress))
                
                if distance_from_center > max_orbit_radius + (ITEM_FADEOUT_RADIUS * 2):
                    self.spawn_ball()
        
        self.spawn_item()
        
        for item in self.items[:]:
            item.update()
            
            distance_from_center = math.sqrt((item.x - self.center_x)**2 + (item.y - self.center_y)**2)
            max_orbit_radius = self.get_max_orbit_radius()
            
            if distance_from_center > max_orbit_radius + ITEM_FADEOUT_RADIUS:
                fade_progress = (distance_from_center - (max_orbit_radius + ITEM_FADEOUT_RADIUS)) / ITEM_FADEOUT_RADIUS
                fade_progress = min(1.0, max(0.0, fade_progress))
                item.alpha = int(255 * (1.0 - fade_progress))
                
                if distance_from_center > max_orbit_radius + (ITEM_FADEOUT_RADIUS * 2):
                    self.items.remove(item)
                    continue
            
            for player in self.players:
                if item.check_collision_with_player(player):
                    keep_item = item.handle_collision(player)
                    if not keep_item:
                        self.items.remove(item)
                        break
                    
            if hasattr(item, 'remove_me') and item.remove_me:
                self.items.remove(item)
    
    def get_max_orbit_radius(self):
        max_radius = BASE_ORBIT_DISTANCE
        for i, player in enumerate(self.orbit_slots):
            if player is not None:
                orbit_radius = BASE_ORBIT_DISTANCE + i * ORBIT_SPACING
                max_radius = max(max_radius, orbit_radius)
        return max_radius
    
    def draw(self):
        self.screen.fill(BLACK)
        
        for i, player in enumerate(self.orbit_slots):
            if player is not None:
                radius = BASE_ORBIT_DISTANCE + i * ORBIT_SPACING
                start_angle = math.radians(135 - 180)
                arc_rect = pygame.Rect(self.center_x - radius, self.center_y - radius, radius * 2, radius * 2)
                pygame.draw.arc(self.screen, ORBIT_COLOR, arc_rect, start_angle, start_angle + math.radians(270), 1)
        
        pygame.draw.circle(self.screen, (50, 50, 50), (self.center_x, self.center_y), 5)
        
        for player in self.players:
            player.draw(self.screen)
        
        if self.ball:
            self.ball.draw(self.screen)
        
        for item in self.items:
            item.draw(self.screen)
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        for flash_item in self.flash_items:
            flash_item.draw(self.screen)
        
        if self.players:
            show_progress = self.chain_hits > 0
            required_players = max(1, len(self.players))
            
            if show_progress:
                progress = len(self.chain_players) / required_players
                bar_width = 200
                bar_height = 20
                bar_x = 20
                bar_y = 70
                
                pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, int(bar_width * progress), bar_height))
                pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
                
                chain_text = self.small_font.render(f"+{self.chain_hits}", True, WHITE)
                self.screen.blit(chain_text, (bar_x + bar_width + 10, bar_y + 2))
            
            y_offset = 105
            for player in self.players:
                player_text = self.small_font.render(player.name, True, player.color)
                self.screen.blit(player_text, (20, y_offset))
                
                if player.id in self.chain_players:
                    hit_text = self.small_font.render("+1", True, WHITE)
                    text_width = player_text.get_width()
                    self.screen.blit(hit_text, (20 + text_width + 10, y_offset))
                
                y_offset += 25
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()