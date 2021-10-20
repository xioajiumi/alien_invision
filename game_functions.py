# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:05:14 2020

@author: Administrator
"""
import pygame
import json
from bullet import Bullet
from alien import Alien
from time import sleep
from random import randint


def check_events(ai_settings, screen,stats, play_button,ship,aliens,
                 bullets,score_board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            store_score_data(stats)
            exit()
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, play_button,
                         ship,aliens, bullets,score_board)
        if event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats, play_button,
                      ship, aliens,bullets,mouse_x, mouse_y,score_board)


def check_keydown_events(event, ai_settings, screen, status, play_button,
                         ship,aliens, bullets,score_board):
    if event.key == pygame.K_q:
        store_score_data(status)
        exit()
    if status.game_active:
        if event.key == pygame.K_d:
            ship.moving_right = True
        if event.key == pygame.K_a:
            ship.moving_left = True
        if event.key == pygame.K_w:
            ship.moving_up = True
        if event.key == pygame.K_s:
            ship.moving_down = True
        if event.key == pygame.K_j:
            fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_p:
        if not status.game_active:
            start_game(ai_settings, screen, status, ship, aliens, bullets,score_board)
    if event.key == pygame.K_r:
        status.game_active = not status.game_active
    if event.key == pygame.K_SPACE:
        ai_settings.change_color = not ai_settings.change_color

def check_keyup_events(event, ship):
    if event.key == pygame.K_d:
        ship.moving_right = False
    if event.key == pygame.K_a:
        ship.moving_left = False
    if event.key == pygame.K_w:
        ship.moving_up = False
    if event.key == pygame.K_s:
        ship.moving_down = False

def check_highest_score(stats, score_board):
    if stats.score >= stats.highest_score:
        stats.highest_score = stats.score



def check_bullets_aliens_collision(ai_settings, screen, ship,stats,score_board,
                                   aliens, bullets):
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collision:
        for aliens in collision.values():
            stats.score += ai_settings.alien_point*len(aliens)
            check_highest_score(stats, score_board)
        score_board.prep_score()


def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets,score_board):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom  >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets,score_board)
            break


def change_fleet_diretion(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edge(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_diretion(ai_settings, aliens)
            break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets,score_board):
    check_fleet_edge(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets,score_board)
    check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets,score_board)

def create_alien(ai_settings, screen, aliens, alien_number, row_numbers):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.rect.x = 2 * alien_width * alien_number+1
    alien.rect.y = alien_height * row_numbers
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, score_board):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
    score_board.show_ships_left()



def check_play_button(ai_settings,screen,stats, play_button,
                      ship, aliens,bullets, mouse_x, mouse_y,score_board):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings,screen,stats,ship, aliens,bullets,score_board)


def start_game(ai_settings,screen,stats,ship, aliens,bullets,score_board):
    stats.highest_score = read_score()
    stats.reset_stats()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens,score_board)
    ship.center_ship()
    pygame.mouse.set_visible(False)
    ai_settings.initialize_dynamic_settings()
    stats.game_active = True

def store_score_data(stats):
    filename = 'score_data.json'
    with open(filename, 'w') as fo:
        json.dump(stats.highest_score, fo)

def read_score():
    filename = 'score_data.json'
    try:
        with open(filename) as fo:
            score = json.load(fo)
    except FileNotFoundError:
        return 0
    else:
        return score

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets,score_board):
    if stats.ship_left > 1:
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens, score_board)
        ship.center_ship()
        stats.ship_left -= 1
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)



def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 3* alien_width
    number_aliens_x = int(available_space_x /(2.5*alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - alien_height - ship_height
    number_rows = int(available_space_y/2/alien_height)
    return number_rows



def update_bullets(ai_settings, screen,ship,stats, score_board,
                   aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if ai_settings.change_color:
            bullet.color = randint(0, 255), randint(0, 255), randint(0, 255)
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen,ship, aliens,score_board)
        stats.level += 1
    check_bullets_aliens_collision(ai_settings, screen, ship,stats,score_board,
                                   aliens, bullets)


def update_screen(screen, ship,stats, score_board, aliens, bullets,
                  background, play_button):
    screen.blit(background, (0, 0))
    ship.update()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    for alien in aliens.sprites():

        alien.blitme()
    #aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()
    score_board.show_score()
    pygame.display.update()

