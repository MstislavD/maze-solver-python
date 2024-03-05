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
        self.visited = False

    def draw(self, color):
        x1 = self._p1.x
        y1 = self._p1.y
        x2 = self._p2.x
        y2 = self._p2.y
        color_by_wall_existance = {True : color, False : "#d9d9d9"}
        self._window.draw_line(Line(Point(x1, y1), Point(x2, y1)), color_by_wall_existance[self.has_top_wall])
        self._window.draw_line(Line(Point(x2, y1), Point(x2, y2)), color_by_wall_existance[self.has_right_wall])
        self._window.draw_line(Line(Point(x2, y2), Point(x1, y2)), color_by_wall_existance[self.has_bottom_wall])
        self._window.draw_line(Line(Point(x1, y2), Point(x1, y1)), color_by_wall_existance[self.has_left_wall])

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
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, seed=None, win=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()

        if not seed==None:
            random.seed(seed)
        self.break_walls_r(0,0)
        self._reset_visited()

    def solve(self):
        self._solve_r(0,0)

    def _create_cells(self):
        width = 2
        for i in range(0, self.num_cols):
            self._cells.append([])
            for j in range(0, self.num_rows):
                p1 = Point(i * self.cell_size_x + self.x1, j * self.cell_size_y + self.y1)
                p2 = Point((i + 1) * self.cell_size_x + self.x1, (j + 1) * self.cell_size_y + self.y1)
                cell = Cell(self.win, p1, p2)
                self._cells[i].append(cell)

        if self.win:   
            for i in range(0, len(self._cells)):
                for j in range(0, len(self._cells[i])):
                    self._draw_cell(i, j)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(0,0)
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        self._draw_cell(i,j)
        
        while(True):
            unvisited_neighbors = []

            neighbors = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
            for n in neighbors:
                if -1 < n[0] < self.num_cols and -1 < n[1] < self.num_rows and not self._cells[n[0]][n[1]].visited:
                    unvisited_neighbors.append(n)    
        
            range = len(unvisited_neighbors)
            if range == 0:
                return 
            break_wall = unvisited_neighbors[random.randint(0, range-1)]
            self._break_wall(i, j, break_wall[0], break_wall[1])
            self.break_walls_r(break_wall[0], break_wall[1])

    def _break_wall(self, x1, y1, x2, y2):
        if x1 < x2:
            self._cells[x1][y1].has_right_wall = False
            self._cells[x2][y2].has_left_wall = False
        elif x1 > x2:
            self._cells[x1][y1].has_left_wall = False
            self._cells[x2][y2].has_right_wall = False
        elif y1 < y2:
            self._cells[x1][y1].has_bottom_wall = False
            self._cells[x2][y2].has_top_wall = False
        elif y1 > y2:
            self._cells[x1][y1].has_top_wall = False
            self._cells[x2][y2].has_bottom_wall = False

    def _reset_visited(self):
        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()
        cell = self._cells[i][j]
        cell.visited = True
        if i==self.num_cols-1 and j==self.num_rows-1:
            return True

        directions = [
            (i - 1, j, lambda: cell.has_left_wall),
            (i + 1, j, lambda: cell.has_right_wall),
            (i, j - 1, lambda: cell.has_top_wall),
            (i, j + 1, lambda: cell.has_bottom_wall)]
        for d in directions:
            if -1 < d[0] < self.num_cols and -1 < d[1] < self.num_rows and not self._cells[d[0]][d[1]].visited and not d[2]():
                cell.draw_move(self._cells[d[0]][d[1]])
                move = self._solve_r(d[0], d[1])
                if move:
                    return True
                cell.draw_move(self._cells[d[0]][d[1]], True)
        return False           
        
        
    def _draw_cell(self, i, j):
        self._cells[i][j].draw("black")
        self._animate()
    
    def _animate(self):
        num_seconds = 1
        self.win.redraw()
        time.sleep(num_seconds / self.num_cols / self.num_rows)
            

def main():
    ratio = 2
    win = Window(800, 600)
    width = 5
    grid_width = 15 * ratio
    grid_height = 10 * ratio
    cell_size = 50 / ratio
    seed = None
    maze = Maze(width, width, grid_height, grid_width, cell_size, cell_size, seed, win)
    maze.solve()
    win.wait_for_close()

main()
