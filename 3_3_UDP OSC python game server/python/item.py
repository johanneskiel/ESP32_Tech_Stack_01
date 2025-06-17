import pygame
import math
import random

WHITE = (255, 255, 255)
RED = (255, 100, 100)
BLUE = (100, 100, 255)

class Item:
    def __init__(self, center_x, center_y, radius=5, speed=2):
        self.x = center_x
        self.y = center_y
        self.radius = radius
        self.speed = speed
        angle = random.uniform(0, 2 * math.pi)
        self.vel_x = self.speed * math.cos(angle)
        self.vel_y = self.speed * math.sin(angle)
        self.color = WHITE
        self.alpha = 255
        self.remove_me = False
        self.original_radius = radius
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
    def draw(self, screen):
        if self.alpha < 255:
            temp_surface = pygame.Surface((self.radius * 2 + 2, self.radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*self.color, self.alpha), 
                             (self.radius + 1, self.radius + 1), self.radius)
            screen.blit(temp_surface, (int(self.x - self.radius - 1), int(self.y - self.radius - 1)))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def start_collision_effect(self):
        pass
    
    def check_collision_with_player(self, player):
        capsule_length = max(0, player.width - 2 * player.capsule_radius)
        
        draw_angle = player.angle + math.pi/2
        cos_a = math.cos(draw_angle)
        sin_a = math.sin(draw_angle)
        
        if capsule_length > 0:
            half_length = capsule_length / 2
            
            center1_x = player.x - half_length * cos_a
            center1_y = player.y - half_length * sin_a
            center2_x = player.x + half_length * cos_a
            center2_y = player.y + half_length * sin_a
            
            dist1 = math.sqrt((self.x - center1_x)**2 + (self.y - center1_y)**2)
            dist2 = math.sqrt((self.x - center2_x)**2 + (self.y - center2_y)**2)
            
            collision_radius = self.radius + player.capsule_radius
            
            if dist1 <= collision_radius or dist2 <= collision_radius:
                return True
            
            rel_x = self.x - player.x
            rel_y = self.y - player.y
            
            local_x = rel_x * cos_a + rel_y * sin_a
            local_y = -rel_x * sin_a + rel_y * cos_a
            
            closest_x = max(-half_length, min(half_length, local_x))
            closest_y = max(-player.capsule_radius, min(player.capsule_radius, local_y))
            
            dist_x = local_x - closest_x
            dist_y = local_y - closest_y
            distance_squared = dist_x * dist_x + dist_y * dist_y
            
            return distance_squared <= (self.radius * self.radius)
        else:
            dist = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
            return dist <= (self.radius + player.capsule_radius)

    def handle_collision(self, player):
        pass


class Ball(Item):
    def __init__(self, center_x, center_y):
        super().__init__(center_x, center_y, radius=5, speed=5)
        self.color = WHITE
        self.bounce_effect_timer = 0
        self.bounce_effect_scale = 1.0
        
    def update(self):
        super().update()
        
        if self.bounce_effect_timer > 0:
            self.bounce_effect_timer -= 1
            progress = self.bounce_effect_timer / 15.0
            self.bounce_effect_scale = 1.0 + 1.0 * progress
        else:
            self.bounce_effect_scale = 1.0
    
    def draw(self, screen):
        radius = int(self.original_radius * self.bounce_effect_scale)
        if self.alpha < 255:
            temp_surface = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*self.color, self.alpha), 
                             (radius + 1, radius + 1), radius)
            screen.blit(temp_surface, (int(self.x - radius - 1), int(self.y - radius - 1)))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), radius)
    
    def start_collision_effect(self):
        self.bounce_effect_timer = 15
        
    def handle_collision(self, player):
        self.start_collision_effect()
        
        collision_point, normal_x, normal_y = self.get_collision_point_and_normal(player)
        
        if normal_x == 0 and normal_y == 0:
            return False
        
        dot_product = self.vel_x * normal_x + self.vel_y * normal_y
        
        self.vel_x = self.vel_x - 2 * dot_product * normal_x
        self.vel_y = self.vel_y - 2 * dot_product * normal_y
        
        self.vel_x *= 1.05
        self.vel_y *= 1.05
        
        angle_variation = random.uniform(-0.2, 0.2)
        cos_var = math.cos(angle_variation)
        sin_var = math.sin(angle_variation)
        
        new_vel_x = self.vel_x * cos_var - self.vel_y * sin_var
        new_vel_y = self.vel_x * sin_var + self.vel_y * cos_var
        
        self.vel_x = new_vel_x
        self.vel_y = new_vel_y
        
        safe_distance = self.original_radius + 2
        self.x = collision_point[0] + normal_x * safe_distance
        self.y = collision_point[1] + normal_y * safe_distance
        
        return True

    def get_collision_point_and_normal(self, player):
        capsule_length = max(0, player.width - 2 * player.capsule_radius)
        
        draw_angle = player.angle + math.pi/2
        cos_a = math.cos(draw_angle)
        sin_a = math.sin(draw_angle)
        
        if capsule_length > 0:
            half_length = capsule_length / 2
            
            center1_x = player.x - half_length * cos_a
            center1_y = player.y - half_length * sin_a
            center2_x = player.x + half_length * cos_a
            center2_y = player.y + half_length * sin_a
            
            dist1 = math.sqrt((self.x - center1_x)**2 + (self.y - center1_y)**2)
            dist2 = math.sqrt((self.x - center2_x)**2 + (self.y - center2_y)**2)
            
            collision_radius = self.radius + player.capsule_radius
            
            if dist1 <= collision_radius:
                if dist1 > 0:
                    normal_x = (self.x - center1_x) / dist1
                    normal_y = (self.y - center1_y) / dist1
                else:
                    normal_x, normal_y = 1, 0
                
                collision_point = (center1_x + normal_x * player.capsule_radius,
                                center1_y + normal_y * player.capsule_radius)
                return collision_point, normal_x, normal_y
                
            elif dist2 <= collision_radius:
                if dist2 > 0:
                    normal_x = (self.x - center2_x) / dist2
                    normal_y = (self.y - center2_y) / dist2
                else:
                    normal_x, normal_y = 1, 0
                
                collision_point = (center2_x + normal_x * player.capsule_radius,
                                center2_y + normal_y * player.capsule_radius)
                return collision_point, normal_x, normal_y
            
            else:
                rel_x = self.x - player.x
                rel_y = self.y - player.y
                
                local_x = rel_x * cos_a + rel_y * sin_a
                local_y = -rel_x * sin_a + rel_y * cos_a
                
                closest_x = max(-half_length, min(half_length, local_x))
                closest_y = max(-player.capsule_radius, min(player.capsule_radius, local_y))
                
                world_closest_x = player.x + closest_x * cos_a + closest_y * (-sin_a)
                world_closest_y = player.y + closest_x * sin_a + closest_y * cos_a
                
                dx = self.x - world_closest_x
                dy = self.y - world_closest_y
                dist = math.sqrt(dx*dx + dy*dy)
                
                if dist > 0:
                    normal_x = dx / dist
                    normal_y = dy / dist
                else:
                    if abs(local_y) > abs(local_x - closest_x):
                        normal_x = -sin_a if local_y > 0 else sin_a
                        normal_y = cos_a if local_y > 0 else -cos_a
                    else:
                        normal_x = cos_a if local_x > 0 else -cos_a
                        normal_y = sin_a if local_x > 0 else -sin_a
                
                return (world_closest_x, world_closest_y), normal_x, normal_y
        
        else:
            dist = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
            if dist > 0:
                normal_x = (self.x - player.x) / dist
                normal_y = (self.y - player.y) / dist
            else:
                normal_x, normal_y = 1, 0
            
            collision_point = (player.x + normal_x * player.capsule_radius,
                            player.y + normal_y * player.capsule_radius)
            return collision_point, normal_x, normal_y


class Power(Item):
    def __init__(self, center_x, center_y, item_type):
        super().__init__(center_x, center_y, radius=8, speed=1.5)
        self.type = item_type
        self.growth_timer = 0
        self.fade_timer = 0
        self.collision_triggered = False
        
    def update(self):
        if not self.collision_triggered:
            super().update()
        
        if self.growth_timer > 0:
            self.growth_timer -= 1
            progress = (20 - self.growth_timer) / 20.0
            self.radius = int(self.original_radius * (1.0 + 2.0 * progress))
        
        if self.fade_timer > 0:
            self.fade_timer -= 1
            progress = self.fade_timer / 30.0
            self.alpha = int(255 * progress)
            
            if self.fade_timer <= 0:
                self.remove_me = True
    
    def start_collision_effect(self):
        if not self.collision_triggered:
            self.collision_triggered = True
            self.growth_timer = 20
            self.fade_timer = 30
        
    def handle_collision(self, player):
        if not self.collision_triggered:
            self.apply_effect(player)
            self.start_collision_effect()
        return True
    
    def apply_effect(self, player):
        pass


class PowerUp(Power):
    def __init__(self, center_x, center_y):
        super().__init__(center_x, center_y, 'blue')
        self.color = BLUE
        self.x = center_x + random.randint(-20, 20)
        self.y = center_y + random.randint(-20, 20)
        
    def apply_effect(self, player):
        player.resize(1.2)


class PowerDown(Power):
    def __init__(self, center_x, center_y):
        super().__init__(center_x, center_y, 'red')
        self.color = RED
        self.x = center_x + random.randint(-20, 20)
        self.y = center_y + random.randint(-20, 20)
        
    def apply_effect(self, player):
        player.resize(0.8)