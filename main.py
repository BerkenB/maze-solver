from graphics import *
from cell import *
from maze import *


def main():
    win = Window(1500, 900)

    maze = Maze(100, 100, 15, 30, 40, 40, win)
    maze.solve()

    
    
    win.wait_for_close()
   



if __name__ == "__main__":
    main()        