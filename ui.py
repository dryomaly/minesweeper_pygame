import pygame as pg
from const import *

class Button:
    def __init__(self, x, y, w, h, 
                text, 
                text_color,
                color, 
                font,
                radius=8
              ):
        self.rect = pg.Rect(x, y, w, h)
        self.text_color = text_color
        self.color = color
        self.font = font
        self.text = font.render(text, True, text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.radius = radius

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, border_radius=self.radius)
        screen.blit(self.text, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
