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

easy_game_board = Board(8, 8, 40, 10)
medium_game_board = Board(15, 15, 40, 35)
# hard_game_board = Board(20, 20, 40) # Выходит за рамки - переделать

overlay = pg.Surface((WIDTH, HEIGHT))
overlay.fill(COLOR_DARKENING_BG)
overlay.set_alpha(120)

# 'menu', 'settings', 'game'
screen_state = 'menu'
# 'ongoing', 'lost', 'won'
game_screen_state = 'ongoing'


button_play = Button((WIDTH - 250) // 2, 300, 250, 80, 
                     'ИГРАТЬ',
                     COLOR_BLACK_FONT,
                     COLOR_PLAY_BUTTON,
                     pg.font.SysFont('Arial', 28)
                    )
button_settings = Button((WIDTH - 200) // 2, 410, 200, 65, 
                     'настройки',
                     COLOR_BLACK_FONT,
                     COLOR_SETTINGS_BUTTON,
                     pg.font.SysFont('Arial', 28)
                    )
button_exit = Button((WIDTH - 160) // 2, 600, 160, 40, 
                     'ВЫХОД',
                     COLOR_BLACK_FONT,
                     COLOR_EXIT_BUTTON,
                     pg.font.SysFont('Arial', 18)
                    )
button_back_menu = Button(20, 20, 120, 60,
                     '< Меню',
                     COLOR_BLACK_FONT,
                     COLOR_BACK_BUTTON,
                     pg.font.SysFont('Arial', 28, True)
                     )
button_restart_game = Button((WIDTH - 200) // 2, 500, 200, 65,
                     'НОВАЯ ИГРА',
                     COLOR_BLACK_FONT,
                     COLOR_RESTART_BUTTON_BG,
                     pg.font.SysFont('Arial', 28, True)
                     )


bg_image_1 = load_img("Images/MENU_BG.png", (WIDTH, HEIGHT))

game_name_image = load_img("Images/GAME_NAME.png")
game_name_image = pg.transform.smoothscale(game_name_image, (600, 200))
game_name_rect = game_name_image.get_rect(midbottom=(WIDTH // 2, button_play.rect.top - 60))

wasted_image = pg.image.load("Images/WASTED.png").convert_alpha()
wasted_image = pg.transform.scale(wasted_image, (WIDTH, HEIGHT))

mission_passed_image = pg.image.load("Images/PASSED(won).png").convert_alpha()
mission_passed_image = pg.transform.scale(mission_passed_image, (696, 204))
mission_passed_rect= mission_passed_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))


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

            elif screen_state == 'game':

                if button_back_menu.is_clicked(ev.pos):
                    screen_state = 'menu'

                elif game_screen_state == "ongoing":
                    cell_clicked = medium_game_board.clicked_cell(ev.pos)

                    if cell_clicked:
                        count_opened_cells = 0
                        safe_cells = (medium_game_board.rows * medium_game_board.cols) - medium_game_board.mines
                        medium_game_board.open_empty_cells(cell_clicked)

                        if cell_clicked.is_mined == True and cell_clicked.cell_state == "opened":
                            game_screen_state = "lost"
                            medium_game_board.mark_all_mines_on_lost()

                        for line in medium_game_board.cells:
                            for cell in line:
                                if cell.is_mined == False and cell.cell_state == "opened":
                                    count_opened_cells += 1

                        if count_opened_cells == safe_cells:
                            game_screen_state = "won"
                            medium_game_board.mark_all_mines_on_won()
         
                elif button_restart_game.is_clicked(ev.pos):
                    medium_game_board = Board(15, 15, 40, 35)
                    game_screen_state = 'ongoing'

            elif screen_state == 'settings':
                if button_back_menu.is_clicked(ev.pos):
                    screen_state = 'menu'

        elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 3:
            if screen_state == 'game' and game_screen_state == "ongoing":
                cell = medium_game_board.clicked_cell(ev.pos)
                if cell:
                    cell.toggle_flag()


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
        screen.fill(COLOR_GAME_BG)
        # easy_game_board.draw(screen)
        medium_game_board.draw(screen)
        # hard_game_board.draw(screen)    
        button_back_menu.draw(screen)

        if game_screen_state == "lost":
            screen.blit(overlay, (0, 0))
            screen.blit(wasted_image, (0, 0))
            button_back_menu.draw(screen)
            button_restart_game.draw(screen)

        elif game_screen_state == "won":
            screen.blit(overlay, (0, 0))
            screen.blit(mission_passed_image, mission_passed_rect)
            button_back_menu.draw(screen)
            button_restart_game.draw(screen)




    elif screen_state == 'settings':
        screen.fill((40, 40, 40))
        button_back_menu.draw(screen)


    # 3. ПОКАЗАТЬ КАДР
    pg.display.flip()
    clock.tick(FPS)