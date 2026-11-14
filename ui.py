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

# class MenuButtons:
#     def __init__(self, font):
#         self.play = Button((WIDTH - 200) // 2, 170, 200, 60, 
#                      'ИГРАТЬ',
#                      pg.Color('black'),
#                      pg.Color(127, 255, 0),
#                      pg.font.SysFont('Arial', 28)
#                     )
#         self.settings = Button((WIDTH - 160) // 2, 240, 160, 40, 
#                      'настройки',
#                      pg.Color('black'),
#                      pg.Color('grey'),
#                      pg.font.SysFont('Arial', 18)
#                     )
#         self.exit = Button((WIDTH - 160) // 2, 330, 160, 40, 
#                      'ВЫХОД',
#                      pg.Color('black'),
#                      pg.Color(255, 69, 0),
#                      pg.font.SysFont('Arial', 18)
#                     )


