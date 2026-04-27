# ValoGuard.py - Anti-AFK tool for VALORANT
# MIT License - Copyright (c) 2026 Qode
# See LICENSE file for full license text

from pynput import keyboard
from pynput.keyboard import Key, Controller
import random
import time
from datetime import datetime
import ctypes
import os
import subprocess

LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "log.txt")
RUN_SECONDS = 4800  # 80 minutes
MOVE_HOLD_SECONDS = 2
MOVE_PAUSE_SECONDS = 1
LISTENER_LOOP_DELAY = 0.2
PANEL_RELOAD_DELAY = 2
STARTUP_DELAY = 3

MOVE_ACTIONS = [
    ("FORWARD", "w"),
    ("BACKWARDS", "s"),
    ("LEFT", "a"),
    ("RIGHT", "d"),
    ("UP", Key.space),
]

LOGO = r"""
                                 __      __   _        _____                     _ 
                                 \ \    / /  | |      / ____|                   | |
                                  \ \  / /_ _| | ___ | |  __ _   _  __ _ _ __ __| |
                                   \ \/ / _` | |/ _ \| | |_ | | | |/ _` | '__/ _` |
                                    \  / (_| | | (_) | |__| | |_| | (_| | | | (_| |
                                     \/ \__,_|_|\___/ \_____|\__,_|\__,_|_|  \__,_|
                                                  
                                                  
"""

# VARS
k_board = Controller()
global user_input
global status


def load_panel():
    if os.name in ('nt', 'dos'):
        subprocess.run(["cmd", "/c", "cls"], check=False)
        try:
            ctypes.windll.kernel32.SetConsoleTitleW("ValoGuard")
        except Exception:
            pass
    else:
        subprocess.run(["clear"], check=False)
    print(LOGO)
    print(
        "      ───────────────────────────────────────────────────────────────────────────────────────────────────────────")
    print(
        "              Never get AFK penalties again by using ValoGuard, the best anti-AFK optimised for VALORANT         ")
    print(
        "      ───────────────────────────────────────────────────────────────────────────────────────────────────────────")
    print(
        "                                                         Usage:                                                  ")
    print(
        "      -----------------------------------------------------------------------------------------------------------")
    print(
        "                                               Press * to start ValoGuard                                        ")
    print(
        "                                          Close this window to stop ValoGuard                                    ")
    print(
        "      ───────────────────────────────────────────────────────────────────────────────────────────────────────────")
    return


def current_time_str():
    return datetime.now().strftime("%H:%M:%S%p")


# CONTROL KEYBOARD
def perform_movement(key_to_press):
    k_board.press(key_to_press)
    time.sleep(MOVE_HOLD_SECONDS)
    k_board.release(key_to_press)
    time.sleep(MOVE_PAUSE_SECONDS)


def write_to_team(message):
    k_board.press(Key.enter)
    time.sleep(0.2)
    k_board.release(Key.enter)
    time.sleep(0.2)
    k_board.type(message)
    k_board.press(Key.enter)
    time.sleep(0.2)
    k_board.release(Key.enter)
    return


def write_to_global(message):
    k_board.press(Key.shift)
    k_board.press(Key.enter)
    time.sleep(0.2)
    k_board.release(Key.shift)
    k_board.release(Key.enter)
    time.sleep(0.2)
    k_board.type(message)
    k_board.press(Key.enter)
    time.sleep(0.2)
    k_board.release(Key.enter)
    return


# RANDOM MOVEMENT
def move(index):
    try:
        action, key_to_press = MOVE_ACTIONS[index]
    except IndexError:
        return "ERROR: Index out of range"
    perform_movement(key_to_press)
    return action


def logger(timestamp, action, info):
    check_files()
    text = "[" + timestamp + "] action: " + action + " -> " + info
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(text + "\n")
    return


def status_logger(text):
    check_files()
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(text + "\n")
    return


def check_files():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "a", encoding="utf-8"):
            pass


def on_press(key):
    global user_input
    try:
        key_char = getattr(key, "char", None)
        if key_char == "*":
            user_input = key_char
            return False
    except Exception as error:
        status_logger("[" + current_time_str() + "] ERROR: " + str(error))


def on_release(key):
    if key == keyboard.Key.esc:
        return False


def wait_for_user_input():
    global status
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()
    try:
        if user_input == "*":
            check_files()
            if status is False:
                start_time = time.monotonic()
                print("[" + current_time_str() + "] Started ValoGuard")
                print("[" + current_time_str() + "] Check " + LOG_FILE + " for more info about actions made by ValoGuard")
                print("[" + current_time_str() + "] ValoGuard will run for 80 minutes and then stop automatically")
                status = True
                action_count = 0
                status_logger("[" + current_time_str() + "] ValoGuard started")
                while status is True:
                    time.sleep(LISTENER_LOOP_DELAY)
                    if (time.monotonic() - start_time) > RUN_SECONDS:
                        status_logger("[" + current_time_str() + "] ValoGuard stopped")
                        status = False
                        break
                    index = random.randrange(len(MOVE_ACTIONS))
                    action = move(index)
                    logger(current_time_str(), action, str(action_count))
                    action_count += 1
        else:
            print("[" + datetime.now().strftime("%H:%M%p") + "] pressed: " + user_input)
    except NameError:
        pass


def main():
    global user_input
    user_input = "."
    global status
    status = False
    # VALOGUARD PANEL
    time.sleep(STARTUP_DELAY)
    load_panel()
    check_files()
    # CREATE LOG FILE
    with open(LOG_FILE, "w", encoding="utf-8") as log_file:
        log_file.write("[" + current_time_str() + "] ValoGuard is ready to start\n")
    # HOTKEY-HANDLER
    while True:
        user_input = "."
        check_files()
        # START LISTENER
        wait_for_user_input()
        time.sleep(PANEL_RELOAD_DELAY)
        load_panel()


if __name__ == "__main__":
    main()
