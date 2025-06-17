import pygame
import math

class Player:
    def __init__(self, player_id, orbit_distance):
        self.id = player_id
        self.name = f"Player_{player_id}"
        self.width = 75
        self.height = 20
        self.min_width = 75
        self.max_width = 150
        self.capsule_radius = self.height / 2
        self.color = (200, 200, 200)
        self.dist = orbit_distance
        self.angle = self.potentiometer_to_absolute(135.0)
        self.target_angle = self.angle
        self.center_x = 0
        self.center_y = 0
        self.x = 0
        self.y = 0
        
    def potentiometer_to_absolute(self, potentiometer_degrees):
        normalized = potentiometer_degrees / 270.0
        absolute_angle = 135.0 + normalized * 270.0
        absolute_angle = absolute_angle % 360.0
        return math.radians(absolute_angle)
    
    def potentiometer_float_to_degrees(self, poti_float):
        poti_float = max(0.0, min(1.0, poti_float))
        return poti_float * 270.0
    
    def set_name_and_color(self, name, color):
        self.name = name
        self.color = color
        
    def set_target_position_float(self, potentiometer_float):
        potentiometer_degrees = self.potentiometer_float_to_degrees(potentiometer_float)
        self.target_angle = self.potentiometer_to_absolute(potentiometer_degrees)
        
    def set_target_position(self, potentiometer_degrees):
        potentiometer_degrees = max(0.0, min(270.0, potentiometer_degrees))
        self.target_angle = self.potentiometer_to_absolute(potentiometer_degrees)
        
    def update_position(self):
        self.x = self.center_x + self.dist * math.cos(self.angle)
        self.y = self.center_y + self.dist * math.sin(self.angle)
    
    def update(self, keys=None, center_x=None, center_y=None):
        if center_x is not None:
            self.center_x = center_x
        if center_y is not None:
            self.center_y = center_y
            
        self.move_towards_target()
        self.update_position()
    
    def move_towards_target(self):
        current_poti = self.absolute_to_potentiometer(self.angle)
        target_poti = self.absolute_to_potentiometer(self.target_angle)
        poti_diff = target_poti - current_poti
        
        if abs(poti_diff) < 0.01:
            self.angle = self.target_angle
            return
        
        distance = abs(poti_diff)
        speed = 0.1 + distance * 0.2
        
        if abs(poti_diff) <= speed:
            current_poti = target_poti
        else:
            current_poti += speed if poti_diff > 0 else -speed
        
        current_poti = max(0.0, min(270.0, current_poti))
        self.angle = self.potentiometer_to_absolute(current_poti)
    
    def absolute_to_potentiometer(self, absolute_angle_rad):
        absolute_deg = math.degrees(absolute_angle_rad) % 360.0
        
        if absolute_deg >= 135.0:
            return absolute_deg - 135.0
        elif absolute_deg <= 45.0:
            return absolute_deg + 225.0
        else:
            return 270.0 if absolute_deg < 90.0 else 0.0
    
    def get_potentiometer_float(self):
        poti_degrees = self.absolute_to_potentiometer(self.angle)
        return poti_degrees / 270.0
    
    def draw(self, screen):
        capsule_length = max(0, self.width - 2 * self.capsule_radius)
        draw_angle = self.angle + math.pi/2
        cos_a = math.cos(draw_angle)
        sin_a = math.sin(draw_angle)
        
        if capsule_length > 0:
            half_length = capsule_length / 2
            center1_x = self.x - half_length * cos_a
            center1_y = self.y - half_length * sin_a
            center2_x = self.x + half_length * cos_a
            center2_y = self.y + half_length * sin_a
            
            perp_cos = -sin_a
            perp_sin = cos_a
            
            rect_points = [
                (center1_x + self.capsule_radius * perp_cos, center1_y + self.capsule_radius * perp_sin),
                (center2_x + self.capsule_radius * perp_cos, center2_y + self.capsule_radius * perp_sin),
                (center2_x - self.capsule_radius * perp_cos, center2_y - self.capsule_radius * perp_sin),
                (center1_x - self.capsule_radius * perp_cos, center1_y - self.capsule_radius * perp_sin)
            ]
            
            pygame.draw.polygon(screen, self.color, rect_points)
            pygame.draw.circle(screen, self.color, (int(center1_x), int(center1_y)), int(self.capsule_radius))
            pygame.draw.circle(screen, self.color, (int(center2_x), int(center2_y)), int(self.capsule_radius))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.capsule_radius))
    
    def resize(self, factor):
        new_width = max(self.min_width, min(self.max_width, self.width * factor))
        self.width = new_width
        self.capsule_radius = self.height / 2