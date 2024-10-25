import curses
from curses import wrapper
import time
import random

THE_CHOICES = [
    "The quick brown fox jumps over the lazy dog, testing typing speed and accuracy.",
    "Typing practice is essential for improving skills, helping you type faster and more accurately.",
    "With consistent practice, you will see improvement in typing speed and accuracy over time.",
    "Learning to type quickly and accurately is an important skill in today's digital world.",
    "Practice makes perfect, so set aside time each day to practice your typing skills.",
    "Focus on accuracy first, then gradually increase your speed to become a proficient typist.",
    "Typing is a skill that can be improved with regular practice and proper finger placement.",
    "Practice typing without looking at the keyboard to develop muscle memory and increase speed.",
    "Use typing software and online resources to find practice exercises and tests for improvement.",
    "Stay motivated by challenging yourself to beat your previous records and enhance productivity."
]

def start(stdscr):
    stdscr.clear()
    stdscr.addstr("Hi there! Welcome to the WPM test.")
    stdscr.addstr("\nPRESS ANY BUTTON TO PLAY")
    stdscr.refresh()
    stdscr.getkey()

def overlapping(stdscr, target, current, wpm=0):
    stdscr.addstr(0, 0, target)
    stdscr.addstr(3, 0, f"WPM: {wpm}")
    stdscr.addstr(2, 0, f"ACCURACY: {accuracy(target, current)}%")
    for i, char in enumerate(current):
        if char == target[i]:
            stdscr.addstr(0, i, char, curses.color_pair(1))
        else:
            stdscr.addstr(0, i, char, curses.color_pair(2))

def accuracy(target, current):
    count = 0
    curr = "".join(current)
    for i in range(len(curr)):
        if target[i] == curr[i]:
            count += 1
    return round((count / len(target)) * 100)

def wpm_test(stdscr):
    target_test = random.choice(THE_CHOICES)
    current_test = []
    stdscr.clear()
    stdscr.addstr(target_test)
    stdscr.refresh()
    wpm = 0

    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_test) / time_elapsed) * 60 / 5)
        
        overlapping(stdscr, target_test, current_test, wpm)
        
        stdscr.refresh()
        if len(current_test) == len(target_test):
            stdscr.nodelay(False)
            break
        try:
            key = stdscr.getkey()
        except:
            continue
        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_test) > 0:
                current_test.pop()
        elif len(current_test) < len(target_test):
            current_test.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr("\nYou did well. PRESS ANY KEY TO CONTINUE")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)
