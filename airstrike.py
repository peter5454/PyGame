import pygame as pg
import constants as c
import math as math
import turrets as t
from airstrike_data import AIRSTRIKE_DATA

class airstrike(pg.sprite.Sprite):
    def __init__(self, airstrike_name):
        super().__init__()
        self.airstrike_name = airstrike_name
        self.type = AIRSTRIKE_DATA.get(airstrike_name, {})
        self.damage = self.type.get("damage")
        self.size = self.type.get("size")
        self.cooldown = self.type.get("cooldown")
        self.cost = self.type.get("cost")
        self.waves = self.type.get("waves")
        self.element = self.type.get("element")
        self.last_shot = 0
        self.shots_fired = 0
        self.running = False
        self.next_shot_time = 0
        self.x = 0
        self.y = 0
        self.frames = self.extract_frames(self.type.get("spritesheet"), 150, 150, 8, 1)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.animation_start_time = 0
        self.animation_playing = False

    def wait(self, wait_time, start_time):
        return pg.time.get_ticks() >= start_time + wait_time

    def place_ability(self, enemy_group, screen):
        current_time = pg.time.get_ticks()
        
        if self.running and self.wait(self.cooldown, self.next_shot_time):
            for enemy in enemy_group:
                if enemy.health > 0:
                    x_dist = enemy.pos[0] - self.x
                    y_dist = enemy.pos[1] - self.y
                    dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                    if dist < self.size:
                        element_damage = t.damage_calc(self.element, enemy)
                        enemy.health -= self.damage * element_damage
                        print(element_damage)
            self.last_shot = current_time
            self.shots_fired += 1
            if self.shots_fired >= self.waves:
                self.running = False
            else:
                self.next_shot_time = current_time

    def start(self, cursor_pos):
        self.x = cursor_pos[0]
        self.y = cursor_pos[1]
        self.running = True
        self.shots_fired = 0
        self.next_shot_time = 0
        self.animation_start_time = pg.time.get_ticks()
        self.animation_playing = True

    def extract_frames(self, spritesheet_path, frame_width, frame_height, columns, rows):
        spritesheet = pg.image.load(spritesheet_path).convert_alpha()
        frames = []
        for row in range(rows):
            for col in range(columns):
                frame_rect = pg.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                frame_image = pg.Surface((frame_width, frame_height), pg.SRCALPHA)
                frame_image.blit(spritesheet, (0, 0), frame_rect)
                frames.append(frame_image)
        return frames

    def play_animation(self, screen, frame_rate=100):
        if not self.animation_playing:
            return
        print(self.type.get("spritesheet"))
        current_time = pg.time.get_ticks()
        if current_time - self.animation_start_time > frame_rate:
            self.animation_start_time = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def is_animation_playing(self):
        return self.animation_playing

    def stop_animation(self):
        self.animation_playing = False
