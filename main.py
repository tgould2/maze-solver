from graphics import Window
from maze import MazeManager


def main():
    screen_x = 800
    screen_y = 600
    win = Window(screen_x, screen_y)
    maze_manager = MazeManager(win, screen_x, screen_y)

    win.wait_for_close()


main()
