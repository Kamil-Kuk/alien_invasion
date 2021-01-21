import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """A class to represent a single star in the background"""

    def __init__(self, ai_settings, screen):
        """Initialize the star and set its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load the star image and get its rect.
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()

    def blitme(self):
        """Draw the star at its current location"""
        self.screen.blit(self.image, self.rect)