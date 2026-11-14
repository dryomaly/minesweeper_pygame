import pygame as pg
from const import *
from ui import *
from board import *

pg.init()

def load_img(path, size=None):
    image = pg.image.load(path).convert_alpha()
    if size:
        image = pg.transform.smoothscale(image, size)
    return image


pg.display.set_caption('Сапёрность')
screen = pg.display.set_mode((WIDTH, HEIGHT))

easy_game_board = Board(8, 8, 40)
medium_game_board = Board(15, 15, 40)
hard_game_board = Board(20, 20, 40)

overlay = pg.Surface((WIDTH, HEIGHT))
overlay.fill(BLACK)
overlay.set_alpha(120)

bg_image_1 = load_img("Images/MENU_BG.png", (WIDTH, HEIGHT))


screen_state = 'menu'


button_play = Button((WIDTH - 250) // 2, 300, 250, 80, 
                     'ИГРАТЬ',
                     pg.Color('black'),
                     pg.Color(127, 255, 0),
                     pg.font.SysFont('Arial', 28)
                    )
button_settings = Button((WIDTH - 200) // 2, 410, 200, 65, 
                     'настройки',
                     pg.Color('black'),
                     pg.Color('grey'),
                     pg.font.SysFont('Arial', 28)
                    )
button_exit = Button((WIDTH - 160) // 2, 600, 160, 40, 
                     'ВЫХОД',
                     pg.Color('black'),
                     pg.Color(255, 69, 0),
                     pg.font.SysFont('Arial', 18)
                    )
button_back_menu = Button(20, 20, 120, 60,
                     '< Меню',
                     pg.Color('black'),
                     pg.Color('grey'),
                     pg.font.SysFont('Arial', 28, True))

game_name_image = load_img("Images/GAME_NAME.png")
w, h = game_name_image.get_size()
game_name_image = pg.transform.smoothscale(game_name_image, (600, 200))
game_name_rect = game_name_image.get_rect(midbottom=(WIDTH // 2, button_play.rect.top - 60))





clock = pg.time.Clock()

while True:
    # 1. СОБЫТИЯ
    for ev in pg.event.get():

        # mouse = pg.mouse.get_pos()

        if ev.type == pg.QUIT:
            pg.quit()
            exit()
        
        elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1: # 1-левая, 2-колесико, 3-правая
            if screen_state == 'menu':
                if button_exit.is_clicked(ev.pos):
                    pg.quit()
                    exit()
                elif button_play.is_clicked(ev.pos):
                    screen_state = 'game'
                elif button_settings.is_clicked(ev.pos):
                    screen_state = 'settings'

            elif screen_state in ('settings', 'game'):
                if button_back_menu.is_clicked(ev.pos):
                    screen_state = 'menu'

    if screen_state == 'menu':
        # ФОН
        screen.blit(bg_image_1, (0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(game_name_image, game_name_rect)
        # КНОПКИ
        button_play.draw(screen)
        button_settings.draw(screen)
        button_exit.draw(screen)

    elif screen_state == 'game':
        screen.fill(BLACK)
        # easy_game_board.draw(screen)
        medium_game_board.draw(screen)
        # hard_game_board.draw(screen)    
        button_back_menu.draw(screen)

    elif screen_state == 'settings':
        screen.fill((40, 40, 40))
        button_back_menu.draw(screen)


    # 3. ПОКАЗАТЬ КАДР
    pg.display.flip()
    clock.tick(FPS)