from tkinter import Tk, BOTH, Canvas
from time import sleep

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_colour="black"):
        line.draw(self.canvas, fill_colour)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_colour):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_colour, width=2)

class Cell:
    def __init__(self, window):
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True
        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1
        self.win = window

    def draw(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        if self.left_wall:
            point1 = Point(self.x1, self.y1)
            point2 = Point(self.x1, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall)
        if self.right_wall:
            point1 = Point(self.x2, self.y1)
            point2 = Point(self.x2, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall)
        if self.top_wall:
            point1 = Point(self.x1, self.y1)
            point2 = Point(self.x2, self.y1)
            wall = Line(point1, point2)
            self.win.draw_line(wall)
        if self.bottom_wall:
            point1 = Point(self.x1, self.y2)
            point2 = Point(self.x2, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall)

    def draw_move(self, to_cell, undo=False):
        colour = "red"
        if undo:
            colour = "gray"
        center1 = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        center2 = Point((to_cell.x1 + to_cell.x2) / 2, (to_cell.y1 + to_cell.y2) / 2)
        line = Line(center1, center2)
        self.win.draw_line(line, fill_colour=colour)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        # self.cells = [[Cell(win) for _ in range(num_cols)] for _ in range(num_rows)]
        self.create_cells()

    def create_cells(self):
        for col in range(self.num_cols):
            cell_col = []
            for row in range(self.num_rows):
                cell = Cell(self.win)
                cell_col.append(cell)
            self.cells.append(cell_col)
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.draw_cell(i, j)

    def draw_cell(self, i, j):
        cell = self.cells[i][j]
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        cell.draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        self.win.redraw()
        sleep(0.03)