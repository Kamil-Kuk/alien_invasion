import sys
import json
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from star import Star
# from rain import Rain
from random import randint


def check_keydown_events(event, ai_settings, screen, sb, stats, ship, aliens, bullets, stars):
    """Respond to keypress"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, sb, stats, ship, aliens, bullets, stars)
    elif event.key == pygame.K_q:
        save_highscore(stats)
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, help_button, ship, aliens, bullets, stars):
    """Respond to keypresses and mouse movements"""
    # Watch for keybord and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_highscore(stats)
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, sb, stats, ship, aliens, bullets, stars)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, stars)
            check_help_button(ai_settings, screen, help_button, stats, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, stars):
    """Start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, sb, stats, ship, aliens, bullets, stars)

def check_help_button(ai_settings, screen, help_button, stats, mouse_x, mouse_y):
    """Displays help if player clicks help"""
    button_clicked = help_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.help_active = True
        show_help(ai_settings, screen, stats)

def start_game(ai_settings, screen, sb, stats, ship, aliens, bullets, stars):
    """Starts a new game and resets previous game stats"""
    # Reset the game statistics and settigns.
    ai_settings.initialize_dynamic_settings()
    stats.reset_stats()
    stats.game_active = True
    reset_screen(ai_settings, screen, sb, aliens, bullets, stars, ship)

def show_help(ai_settings, screen, stats):
    """Displays help"""
    if not stats.game_active and stats.help_active:
        msg = ["Alien Invasion 2020 by Kamil Kukowski",
               "Press 'p' or click 'Play' to start",
               "Press 'q' to quit the game",
               "Press space bar to shoot bullets",
               "Use arrow keys to move the ship"]
        text_color = (255, 255, 255)
        font = pygame.font.SysFont(None, 48)
        for position, line in enumerate(msg):
            help_image = font.render(line, True, text_color, ai_settings.bg_color)
            help_rect = help_image.get_rect()
            screen_rect = screen.get_rect()
            help_rect.centery = screen_rect.centery + 100 + 50 * position
            help_rect.centerx = screen_rect.centerx
            screen.blit(help_image, help_rect)

def reset_screen(ai_settings, screen, sb, aliens, bullets, stars, ship):
    # Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()
    stars.empty()

    #Reset the scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Create a new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    create_star_background(ai_settings, screen, stars)
    ship.center_ship()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    #Update bullet positions
    bullets.update()
    #Get rid of bullets that have disappeard
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def fire_bullets(ai_settings, screen, ship, bullets):
    # Creates a new bullet and add it to the bullet group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fir in a row"""
    available_space_x = ai_settings.screen_width - alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_aliens_y(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fir on the screen"""
    available_space_y = (ai_settings.screen_height - (4 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Creates a full fleet of alines"""
    #Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_aliens_y(ai_settings, ship.rect.height, alien.rect.height)
        #Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_max_number_stars_x(ai_settings, star_width):
    """Determines the maximum number of stars in a row to appear in the background"""
    available_space_x = ai_settings.screen_width - star_width
    max_number_stars_x = int(available_space_x / (7 * star_width))
    return max_number_stars_x

def get_max_number_stars_y(ai_settings, star_height):
    """Determines the maximum number of rows of stars to appear in the background"""
    available_space_y = ai_settings.screen_height - star_height
    max_number_stars_y = int(available_space_y / (7 * star_height))
    return max_number_stars_y

def create_star(ai_settings, screen, stars, star_x, star_y):
    """Creates a star in given coordinates"""
    star = Star(ai_settings, screen)
    star.rect.x = star_x
    star.rect.y = star_y
    stars.add(star)

def create_star_background(ai_settings, screen, stars):
    """Creates a background with stars"""
    star = Star(ai_settings, screen)
    star_y = 0
    max_number_stars_x = get_max_number_stars_x(ai_settings, star.rect.width)
    max_number_stars_y = get_max_number_stars_y(ai_settings, star.rect.height)
    #Generates a random number of rows to appear in the background
    number_rows = randint(5, max_number_stars_y)
    for row_number in range(number_rows):
        star_y += (ai_settings.screen_height) / number_rows
        #Generates a random number of stars to appear in each row
        number_stars_x = randint(4, max_number_stars_x)
        star_x = 0
        for star_number in range(number_stars_x):
            star_x += (ai_settings.screen_width) / number_stars_x
            create_star(ai_settings, screen, stars, star_x, star_y)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, stars, play_button, help_button):
    """Update image on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    #Redraw all bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    stars.draw(screen)
    ship.blitme()
    aliens.draw(screen)

    #Draw the score information
    sb.show_score()

    #Draw the button if the game is active
    if not stats.game_active:
        play_button.draw_button()
        help_button.draw_button()

    show_help(ai_settings, screen, stats)

    # Make the most recently drawn screen visible
    pygame.display.flip()

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, stars):
    """Check if the fleet as at the edge, and then update the position of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, stars)
    #Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, stars)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any alien have reached en edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collision"""
    #Check for any bullets that have git aliens.
    #If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_scores(stats, sb)
    if len(aliens) == 0:
        #Destroy existing bullets, speeds up game and create new fleet, star a new level
        bullets.empty()
        ai_settings.increase_speed()

        #Incease level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, stars):
    """Respond to ship hit by alien"""
    if stats.ship_left > 0:
        #Decrement ships left
        stats.ship_left -=1
        reset_screen(ai_settings, screen, sb, aliens, bullets, stars, ship)
        #Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, stars):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat this as the same as if the ship got hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, stars)
            break

def check_high_scores(stats, sb):
    """Check to see if there's new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def save_highscore(stats):
    """Checks if current score is the all-time high and saves it to a file"""
    filename = 'highscore.json'
    try:
        with open(filename) as f_obj:
            prev_highscore = json.load(f_obj)
    except FileNotFoundError:
        prev_highscore = 0

    if prev_highscore < stats.high_score:
        with open(filename, 'w') as f_obj:
            json.dump(stats.high_score, f_obj)