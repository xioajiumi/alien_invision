import pygame.font
import pygame.sprite
from ship import Ship


class Scoreboard():
    def __init__(self, ai_settiings, screen, stats):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_sttings = ai_settiings
        self.stats = stats
        self.text_color = (130, 230, 30)
        self.font = pygame.font.SysFont(None, 30)

    def prep_score(self):
        rounded_score = round(self.stats.score, -2)
        #score_str = f'{rounded_score}'
        score_str = "{:,}".format(rounded_score)+':present score'
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = self.screen_rect.top

    def prep_highest_score(self):
        rounded_highest_score = round(self.stats.highest_score, -2)
        highest_score_str = "{:,}".format(rounded_highest_score) + ':highest score'
        self.highest_score_image = self.font.render(highest_score_str,
                                                    True, self.text_color)
        self.highest_score_rect = self.score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.screen_rect.top

    def prep_level(self):
        level_str = str(self.stats.level) + ':present  level'
        self.level_image = self.font.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom

    def prep_ships(self):
        self.ships = pygame.sprite.Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_sttings, self.screen)
            ship.rect.y = 50
            ship.rect.right = self.screen_rect.right - ship_number*60
            self.ships.add(ship)

    def show_score(self):
        self.prep_score()
        self.prep_highest_score()
        self.prep_level()
        self.prep_ships()
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highest_score_image, self.highest_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)
        #for ship in self.ships.sprites():
        #    self.screen.blit(ship.image,ship.rect)

    def show_ships_left(self):
        self.prep_ships()
        for ship in self.ships.sprites():
            self.screen.blit(ship.image,ship.rect)


