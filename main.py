import pygame as pg
import getpass
from const import *
from ui import *
from board import *
from stats import load_stats, save_stats

pg.init()


def format_time(time):
    if time == None:
        return "_.___"
    else:
        return f"{time / 1000:.3f}"


pg.display.set_caption("Сапёрность")
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
stats = load_stats()

sound_cell_click = pg.mixer.Sound("Sounds/cellClick.wav")
sound_main_button = pg.mixer.Sound("Sounds/select.wav")
sound_back_button = pg.mixer.Sound("Sounds/deSelect.wav")
sound_flag_placement = pg.mixer.Sound("Sounds/flagPlacement.wav")
sound_boom = pg.mixer.Sound("Sounds/boom.wav")

cur_diff = EASY
current_board = Board(cur_diff[0], cur_diff[1], cur_diff[2], cur_diff[3])

overlay = pg.Surface((WIDTH, HEIGHT))
overlay.fill(COLOR_DARKENING_BG)
overlay.set_alpha(120)

timer_plate = pg.Rect(0, 0, 260, 60)
timer_plate.bottomleft = (20, HEIGHT - 20)

statistics_plate = pg.Rect(0, 0, 550, 650)
statistics_plate.center = (WIDTH // 2, HEIGHT // 2)

# 'menu', 'statistics', 'game'
screen_state = "menu"

# 'ongoing', 'lost', 'won'
game_screen_state = "ongoing"

timer = 0
is_timer_going = False

timer_font = pg.font.SysFont("Comic Sans MS", 28)
statistics_font = pg.font.SysFont("Comic Sans MS", 24)


button_play = Button((WIDTH - 250) // 2, 300, 250, 80, 
                     "ИГРАТЬ",
                     COLOR_BLACK_FONT,
                     COLOR_PLAY_BUTTON,
                     pg.font.SysFont("Comic Sans MS", 28)
                    )
button_statistics = Button((WIDTH - 200) // 2, 410, 200, 65, 
                     "статистика",
                     COLOR_BLACK_FONT,
                     COLOR_STATISTICS_BUTTON,
                     pg.font.SysFont("Comic Sans MS", 28)
                    )
button_exit = Button((WIDTH - 160) // 2, 600, 160, 40, 
                     "ВЫХОД",
                     COLOR_BLACK_FONT,
                     COLOR_EXIT_BUTTON,
                     pg.font.SysFont("Comic Sans MS", 18)
                    )
button_back_menu = Button(20, 20, 120, 60,
                     "< Меню",
                     COLOR_BLACK_FONT,
                     COLOR_BACK_BUTTON,
                     pg.font.SysFont("Comic Sans MS", 28, True)
                     )
button_restart_game = Button((WIDTH - 200) // 2, 500, 200, 65,
                     "НОВАЯ ИГРА",
                     COLOR_BLACK_FONT,
                     COLOR_RESTART_BUTTON_BG,
                     pg.font.SysFont("Comic Sans MS", 28, True)
                     )
button_switch_difficulty_EASY = Button(785, 315, 300, 50, "Сложность: ЛЕГКАЯ", COLOR_BLACK_FONT, COLOR_OPENED_CELL_EMPTY, pg.font.SysFont("Comic Sans MS", 22, True))
button_switch_difficulty_MEDIUM = Button(785, 315, 300, 50, "Сложность: СРЕДНЯЯ", COLOR_BLACK_FONT, COLOR_OPENED_CELL_EMPTY, pg.font.SysFont("Comic Sans MS", 22, True))
button_switch_difficulty_HARD = Button(785, 315, 300, 50, "Сложность: СЛОЖНАЯ", COLOR_BLACK_FONT, COLOR_OPENED_CELL_EMPTY, pg.font.SysFont("Comic Sans MS", 22, True))


bg_image_1 = pg.image.load("Images/MENU_BG.png")

game_name_image = pg.image.load("Images/GAME_NAME.png").convert_alpha()
game_name_image = pg.transform.smoothscale(game_name_image, (600, 200))
game_name_rect = game_name_image.get_rect(midbottom=(WIDTH // 2, button_play.rect.top - 60))

wasted_image = pg.image.load("Images/WASTED.png").convert_alpha()
wasted_image = pg.transform.scale(wasted_image, (WIDTH, HEIGHT))

mission_passed_image = pg.image.load("Images/PASSED(won).png").convert_alpha()
mission_passed_image = pg.transform.scale(mission_passed_image, (696, 204))
mission_passed_rect= mission_passed_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))


def new_game():
    global current_board, game_screen_state, timer, is_timer_going
    current_board = Board(cur_diff[0], cur_diff[1], cur_diff[2], cur_diff[3])
    game_screen_state = "ongoing"
    timer = 0
    is_timer_going = False


while True:
    dt = clock.tick(FPS)
    if is_timer_going and screen_state == "game" and game_screen_state == "ongoing":
        timer += dt

    # 1. СОБЫТИЯ
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            exit()
        
        elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1: # 1-левая, 2-колесико, 3-правая
            if screen_state == "menu":
                if button_exit.is_clicked(ev.pos):
                    pg.quit()
                    exit()
                elif button_play.is_clicked(ev.pos):
                    sound_main_button.play()
                    screen_state = "game"
                elif button_statistics.is_clicked(ev.pos):
                    sound_main_button.play()
                    screen_state = "statistics"
                
                elif button_switch_difficulty_EASY.is_clicked(ev.pos):
                    if cur_diff == EASY:
                        cur_diff = MEDIUM
                    elif cur_diff == MEDIUM:
                        cur_diff = HARD
                    else:
                        cur_diff = EASY
                    sound_main_button.play()
                    new_game()

            elif screen_state == "game":                
                if button_back_menu.is_clicked(ev.pos):
                    sound_back_button.play()
                    screen_state = "menu"

                elif game_screen_state == "ongoing":
                    cell_clicked = current_board.clicked_cell(ev.pos)
                    
                    if cell_clicked:
                        is_timer_going = True
                        was_closed = cell_clicked.cell_state == "closed"
                        current_board.open_empty_cells(cell_clicked)

                        if cell_clicked.is_mined == True and cell_clicked.cell_state == "opened":
                            sound_boom.play()
                            cell_clicked.is_clicked = True
                            game_screen_state = "lost"
                            current_board.mark_all_mines_on_lost()

                        elif was_closed:
                            sound_cell_click.play()

                        count_opened_safe_cells = current_board.count_opened_safe_cells()

                        if current_board.is_game_won():
                            game_screen_state = "won"
                            current_board.mark_all_mines_on_won()
                        
                        if game_screen_state != "ongoing":
                            stats["all_games"] += 1
                            stats["opened_cells"] += count_opened_safe_cells

                            if game_screen_state == "lost":
                                stats["losses"] += 1
                            else:
                                stats["wins"] += 1

                                if cur_diff == EASY:
                                    diff_name = "EASY"
                                elif cur_diff == MEDIUM:
                                    diff_name = "MEDIUM"
                                elif cur_diff == HARD:
                                    diff_name = "HARD"

                                best = stats["best_time"][diff_name]
                                if best == None or timer < best:
                                    stats["best_time"][diff_name] = timer
                            save_stats(stats)
         
                elif button_restart_game.is_clicked(ev.pos):
                    sound_main_button.play()
                    new_game()

            elif screen_state == "statistics":
                if button_back_menu.is_clicked(ev.pos):
                    sound_back_button.play()
                    screen_state = "menu"

        elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 3:
            if screen_state == 'game' and game_screen_state == "ongoing":
                cell = current_board.clicked_cell(ev.pos)
                if cell:
                    if cell.cell_state != "opened":
                        sound_flag_placement.play()
                    is_timer_going = True
                    cell.toggle_flag()


    if screen_state == "menu":
        # ФОН
        screen.blit(bg_image_1, (0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(game_name_image, game_name_rect)

        # КНОПКИ
        button_play.draw(screen)
        button_statistics.draw(screen)
        button_exit.draw(screen)
        if cur_diff == EASY:
            button_switch_difficulty_EASY.draw(screen)
        elif cur_diff == MEDIUM:
            button_switch_difficulty_MEDIUM.draw(screen)
        elif cur_diff == HARD:
            button_switch_difficulty_HARD.draw(screen)

    elif screen_state == "game":
        screen.fill(COLOR_GAME_BG)
        current_board.draw(screen)

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

        pg.draw.rect(screen, COLOR_TIMER_PLATE, timer_plate, border_radius=8)
        timer_str = f"Время: {format_time(timer)}"
        timer_text = timer_font.render(timer_str, True, COLOR_BLACK_FONT)
        timer_text_rect = timer_text.get_rect(midleft=(timer_plate.left + 15, timer_plate.centery))
        screen.blit(timer_text, timer_text_rect)
        
    elif screen_state == "statistics":
        screen.fill(COLOR_STATISTICS_BG)

        y_of_text = statistics_plate.top + Y_STEP_FOR_STATS
        stats_list = [
            f"Сыграно игр: {stats['all_games']}",
            f"Побед: {stats['wins']}",
            f"Поражений: {stats['losses']}",
            f"Открыто клеток: {stats['opened_cells']}",
            "----------------------------------------------------",
            "Лучшее время:",
            f" - Легкая: {format_time(stats['best_time']['EASY'])} с.",
            f" - Средняя: {format_time(stats['best_time']['MEDIUM'])} с.",
            f" - Сложная: {format_time(stats['best_time']['HARD'])} с."
        ]

        pg.draw.rect(screen, COLOR_STATISTICS_FRONT_PLATE, statistics_plate, border_radius=8)

        player_name_str = getpass.getuser()
        player_name_text = statistics_font.render(player_name_str, True, COLOR_LIGHTYELLOW_FONT)
        player_name_text_rect = player_name_text.get_rect(center=(statistics_plate.centerx, statistics_plate.top + 25))
        screen.blit(player_name_text, player_name_text_rect)

        for line in stats_list: 
            stats_text = statistics_font.render(line, True, COLOR_WHITE_FONT)
            stats_text_rect = stats_text.get_rect(topleft=(statistics_plate.left + 15, y_of_text))
            y_of_text += Y_STEP_FOR_STATS
            screen.blit(stats_text, stats_text_rect)

        button_back_menu.draw(screen)


    # 3. ПОКАЗАТЬ КАДР
    pg.display.flip()
