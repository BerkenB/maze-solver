from cell import *
import time
import random
from queue import LifoQueue

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows    
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.cells_for_break_walls = LifoQueue()
        self.cells_for_solve_maze = LifoQueue()
        
        if seed != None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()
    
    def __create_cells(self):
        self.__cells = [[Cell(self.__win) for a in range(self.num_rows)] for b in range(self.num_cols)]

        if self.__win == None:
            return
        
        for j in range(len(self.__cells)):
             for i in range(len(self.__cells[j])):
                 self.__draw_cell(j, i)
                        
    def __draw_cell(self, i, j):
        x = self.x1 + (i * self.cell_size_x)
        y = self.y1 + (j * self.cell_size_y)
        self.__cells[i][j].draw(x, y, x + self.cell_size_x, y + self.cell_size_y)
        self._animate()

    def _animate(self, sleep = 0.0001):
        self.__win.redraw()
        time.sleep(sleep)
    
    def get_cells(self):
        return self.__cells

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        if self.__win == None:
            return
    
        self.__draw_cell(0, 0)
        self.__draw_cell(self.num_cols-1,self.num_rows -1)

    def __break_walls_r(self, i, j):
        if self.__win == None:
            return
        
        current_cell = self.__cells[i][j]
        exit_cell = self.__cells[self.num_cols - 1][self.num_rows -1]
        current_cell.visited = True
        self.cells_for_break_walls.put((i, j))

        if current_cell == exit_cell:
            return
        
        possible_directions = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]
        possible_directions = list(filter(lambda x: x[0] >= 0 and x[0] <= self.num_cols-1
                           and x[1] >= 0 and x[1] <= self.num_rows-1
                           ,possible_directions
                                         )
                                  )
        possible_directions = list(filter(lambda x: self.__cells[x[0]][x[1]].visited == False, possible_directions))

        if possible_directions:
            random_direction = random.choice(possible_directions)
            target_cell = self.__cells[random_direction[0]][random_direction[1]]

            movement_direction = (i - random_direction[0], j - random_direction[1])
            if movement_direction[0] == 1:
                current_cell.has_left_wall = False
                target_cell.has_right_wall = False
            elif movement_direction[0] == -1:
                current_cell.has_right_wall = False
                target_cell.has_left_wall = False
            elif movement_direction[1] == 1:
                current_cell.has_top_wall = False
                target_cell.has_bottom_wall = False
            elif movement_direction[1] == -1:
                current_cell.has_bottom_wall = False
                target_cell.has_top_wall = False
   
            self.__draw_cell(i, j)
            self.__break_walls_r(random_direction[0], random_direction[1])

        else:
            if self.cells_for_break_walls.qsize() >= 2:
                self.cells_for_break_walls.get()
                previous_cell = self.cells_for_break_walls.get()
                self.__break_walls_r(previous_cell[0], previous_cell[1])
            else:
                return 
    
    def __reset_cells_visited(self):
        for columns in self.__cells:
            for cells in columns:
                cells.visited = False

    def solve(self):
        return self.__solve_r()

    def __solve_r(self, i = 0, j = 0):
        current_cell = self.__cells[i][j]
        exit_cell = self.__cells[self.num_cols - 1][self.num_rows -1]
        current_cell.visited = True
        self.cells_for_solve_maze.put((i, j))
        
        if current_cell == self.__cells[self.num_cols-1][self.num_rows-1]:
            return True

        possible_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        possible_directions = list(filter(lambda x: x[0] + i >= 0 and x[0] + i <= self.num_cols-1
                           and x[1] + j >= 0 and x[1] + j <= self.num_rows-1
                           ,possible_directions
                                         )
                                  )
        possible_directions = list(filter(lambda x: self.__cells[i + x[0]][j + x[1]].visited == False, possible_directions))

        def check_walls(x):
            if x[0] == 1 and current_cell.has_right_wall == False:
                return True
            elif x[0] == -1 and current_cell.has_left_wall == False:
                return True
            elif x[1] == 1 and current_cell.has_bottom_wall == False:
                return True
            elif x[1] == -1 and current_cell.has_top_wall == False:
                return True
            else:
                return False
            
        possible_directions = list(filter(check_walls, possible_directions))
        if possible_directions:
            next_direction = possible_directions[0]
            target_cell = self.__cells[i + next_direction[0]][j + next_direction[1]]
            current_cell.draw_move(target_cell)
            self._animate(0.01)
            solved = self.__solve_r(i + next_direction[0], j + next_direction[1])
            if solved:
                return True

        else:
            if self.cells_for_solve_maze.qsize() >= 2:
                current_undo_index = self.cells_for_solve_maze.get()
                traceback_cell_index = self.cells_for_solve_maze.get()
                
                current_undo_cell = self.__cells[current_undo_index[0]][current_undo_index[1]]
                traceback_cell = self.__cells[traceback_cell_index[0]][traceback_cell_index[1]]

                current_undo_cell.draw_move(traceback_cell, undo = True)
                self._animate(0.01)
                solved = self.__solve_r(traceback_cell_index[0], traceback_cell_index[1])
                if solved:
                    return True
                else:
                    return False

            else:
                return False




                

        



    