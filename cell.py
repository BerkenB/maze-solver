from graphics import *

class Cell:
    def __init__(self, win = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win
        self.visited = False
    
    def __repr__(self):
        return f"x1:{self.__x1} y1:{self.__y1} x2:{self.__x2} y2:{self.__y2}"
    
    def draw(self, x1, y1, x2, y2, color = "black"):
        if self.__win is None:
            return
        self.__x1 = x1; self.__y1 = y1
        self.__x2 = x2; self.__y2 = y2

        if self.has_left_wall:
           self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), color)
        elif not self.has_left_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")

        if self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), color)
        elif not self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")

        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), color)
        elif not self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")
        
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), color)

        elif not self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")

    def get_center(self):
        return Point(self.__x1 + (self.__x2 - self.__x1)/2, self.__y1 + (self.__y2 - self.__y1)/2)
    
    def draw_move(self, to_cell, undo=False):
        if self.__win == None:
            return
        center1 = self.get_center()
        center2 = to_cell.get_center()
        line = Line(center1, center2)
        self.__win.draw_line(line, fill_color = "red" if undo == False else "blue")

    


        
