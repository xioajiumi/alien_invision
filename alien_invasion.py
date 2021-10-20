# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:55:50 2020

@author: Administrator
"""
import os
import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from GameStats import GameStats
from pygame.sprite import Group
from button import Button
from Scoreboard import Scoreboard


def run_game():
    x, y= 70, 0
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (x, y)
    pygame.init()
    ai_settings = Settings()
    bullets = Group()
    aliens = Group()
    stats = GameStats(ai_settings)
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    background = pygame.image.load('images/images.jfif')
    background = pygame.transform.smoothscale(background, (900, 700))
    score_board = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    play_button = Button(ai_settings, screen, 'Play')
    gf.create_fleet(ai_settings, screen,ship, aliens,score_board)
    clock = pygame.time.Clock()

    while True:
        gf.check_events(ai_settings, screen,stats,play_button, ship,aliens,
                        bullets,score_board)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen,ship,stats,score_board, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets,score_board)
        gf.update_screen(screen,ship, stats , score_board,
                         aliens, bullets, background, play_button)
        clock.tick(60)


run_game()
