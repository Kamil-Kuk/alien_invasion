import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf

def run_game():
    """Initialize game, settings and creates screen object"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    #Create a group for background stars
    stars = Group()
    #Create background with numerous stars
    gf.create_star_background(ai_settings, screen, stars)
    #Make a ship
    #ship = Ship(ai_settings, screen)
    ship = Ship(ai_settings, screen)
    #Make a group to store bullets in
    bullets = Group()
    #Make group of aliens
    aliens = Group()
    #Create the fleet of aliens
    #gf.create_fleet(ai_settings, screen, ship, aliens)
    #Create an instance to store game statistics.
    stats = GameStats(ai_settings)
    #Make the Play button.
    play_button = Button(ai_settings, screen, "Play", -50)
    #Make the Help button.
    help_button = Button(ai_settings, screen, "Help", +50)
    #Create an instance to stroe game statistics and create scoreboard
    sb = Scoreboard(ai_settings, screen, stats)

    #Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, help_button, ship, aliens, bullets, stars)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, stars)
            #gf.update_rain(rain)

        #gf.update_screen(ai_settings, screen, ship, aliens, bullets, stars, rain)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, stars, play_button, help_button)

run_game()