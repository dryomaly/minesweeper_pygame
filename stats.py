import json
import os

STATS_FILE = "stats.json"


def default_stats():
    stats = {
        "all_games": 0,
        "wins": 0,
        "losses": 0,
        "opened_cells": 0,
        "best_time": {
            "EASY": None,
            "MEDIUM": None,
            "HARD": None
        }
    }

    return stats


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)


def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    else:
        return default_stats()
