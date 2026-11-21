import pygame as pg

# Константины
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Цветастики
COLOR_OPENED_CELL_EMPTY = pg.Color("#fff59e")
COLOR_OPENED_CELL_NUMBER = pg.Color("#ebdd70")
COLOR_CLOSED_CELL_1 = pg.Color("#2a912a")
COLOR_CLOSED_CELL_2 = pg.Color("#278427")
COLOR_MINE_CELL = pg.Color("#000000")
COLOR_MINE_CELL_TOUCHED = pg.Color("#FF0000")
COLOR_CELL_NUMS = {
    1: "#2B2BD1",
    2: "#1E931E",
    3: "#EE1616",
    4: "#00008A",
    5: "#630101",
    6: "#007A67",
    7: "#7500B9",
    8: "#888888"
}

COLOR_BLACK_FONT = pg.Color("#000000")
COLOR_RESTART_BUTTON_BG = pg.Color("#C0C0C0")
COLOR_PLAY_BUTTON = pg.Color("#2BC82B")
COLOR_SETTINGS_BUTTON = pg.Color("#AAAAAA")
COLOR_BACK_BUTTON = pg.Color("#AAAAAA")
COLOR_EXIT_BUTTON = pg.Color("#FF4500")

DARKENING_BG = pg.Color("#000000")
COLOR_GAME_BG = pg.Color("#00b0eb")

