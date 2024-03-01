import random
import time

from tkinter import Tk, BOTH, Canvas

class Window:

    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze solver")
        self.__root.geometry(f"{width}x{height}")

        self.__canvas = Canvas()       
        self.__canvas.config(width = width, height = height)
        self.__canvas.pack()


        self.__window_is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_is_running = True
        while self.__window_is_running:
            self.redraw()
    
    def close(self):
        self.__window_is_running = False

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)    

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=color, width=2)
        canvas.pack()

class Cell:
    def __init__(self, window, p1, p2):
        self._window = window
        self._p1 = p1
        self._p2 = p2
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.has_right_wall = True
        self.has_left_wall = True

    def draw(self, color):
        x1 = self._p1.x
        y1 = self._p1.y
        x2 = self._p2.x
        y2 = self._p2.y
        if self.has_top_wall:
            self._window.draw_line(Line(Point(x1, y1), Point(x2, y1)), color)
        if self.has_right_wall:
            self._window.draw_line(Line(Point(x2, y1), Point(x2, y2)), color)
        if self.has_bottom_wall:
            self._window.draw_line(Line(Point(x2, y2), Point(x1, y2)), color)
        if self.has_left_wall:
            self._window.draw_line(Line(Point(x1, y2), Point(x1, y1)), color)

    def draw_move(self, to_cell, undo=False):
        x1 = (self._p1.x + self._p2.x) / 2
        y1 = (self._p1.y + self._p2.y) / 2
        x2 = (to_cell._p1.x + to_cell._p2.x) / 2
        y2 = (to_cell._p1.y + to_cell._p2.y) / 2
        color = "red"
        if undo:
            color = "gray"
        self._window.draw_line(Line(Point(x1,y1), Point(x2,y2)), color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()


    def _create_cells(self):
        width = 2
        for i in range(0, self.num_cols):
            self._cells.append([])
            for j in range(0, self.num_rows):
                p1 = Point(i * self.cell_size_x + self.x1, j * self.cell_size_y + self.y1)
                p2 = Point((i + 1) * self.cell_size_x + self.x1, (j + 1) * self.cell_size_y + self.y1)
                cell = Cell(self.win, p1, p2)
                self._cells[i].append(cell)
            
        for i in range(0, len(self._cells)):
            for j in range(0, len(self._cells[i])):
                self._draw_cell(i, j)
        
    def _draw_cell(self, i, j):
        self._cells[i][j].draw("black")
        self._animate()
    
    def _animate(self):
        num_seconds = 2
        self.win.redraw()
        time.sleep(num_seconds / self.num_cols / self.num_rows)
            

def main():
    win = Window(800, 600)
    width = 2
    grid_width = 15
    grid_height = 10
    cell_size = 50

    #draw_random_maze(width, grid_width, grid_height, cell_size, win)
    
    maze = Maze(width, width, grid_height, grid_width, cell_size, cell_size, win)

    win.wait_for_close()

def draw_random_maze(width, grid_width, grid_height, cell_size, win):
    cells = []
    undo = False
    random_range = 1

    for i in range(0, grid_width):
        cells.append([])
        for j in range(0, grid_height):
            p1 = Point(i * cell_size + width, j * cell_size + width)
            p2 = Point((i + 1) * cell_size + width, (j + 1) * cell_size + width)
            cell = Cell(win, p1, p2)
            cells[i].append(cell)

            b = random.randint(0, random_range)
            r = random.randint(0, random_range)
            if b == 0:
                cell.has_bottom_wall = False
            if r == 0:
                cell.has_right_wall = False
            if j > 0 and not cells[i][j-1].has_bottom_wall:
                cell.has_top_wall = False
                cell.draw_move(cells[i][j-1], undo)
            if i > 0 and not cells[i-1][j].has_right_wall:
                cell.has_left_wall = False
                cell.draw_move(cells[i-1][j], undo)

            cell.draw("black")


main()
