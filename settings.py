# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 08:57:28 2020

@author: Administrator
"""


class Settings():
    def __init__(self):
        # screen settings
        self.screen_width = 900
        self.screen_height = 700
        self.ship_limit = 3
        self.bullet_width = 15
        self.bullet_height = 5
        self.bullet_color = 207, 0, 112
        self.bullets_allowed = 10
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 20
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        self.alien_point = 500
        #self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.bullet_speed_factor = 5
        self.ship_speed_factor = 3
        self.alien_speed_factor = 5
        self.fleet_direction = 1
        self.alien_point = 500
        self.change_color = False

    def increase_speed(self):
        self.bullet_speed_factor *= self.speedup_scale
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_point = int(self.score_scale *  self.alien_point)


