from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

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
    def __init__(self, window=None):
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True
        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1
        self.visited = False
        self.win = window

    def draw(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        if self.win is None:
            return
        if self.left_wall:
            point1 = Point(self.x1, self.y1)
            point2 = Point(self.x1, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall)
        else:
            point1 = Point(self.x1, self.y1)
            point2 = Point(self.x1, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall, fill_colour="#d9d9d9")
        if self.right_wall:
            point1 = Point(self.x2, self.y1)
            point2 = Point(self.x2, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall)
        else:
            point1 = Point(self.x2, self.y1)
            point2 = Point(self.x2, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall, fill_colour="#d9d9d9")
        if self.top_wall:
            point1 = Point(self.x1, self.y1)
            point2 = Point(self.x2, self.y1)
            wall = Line(point1, point2)
            self.win.draw_line(wall)
        else:
            point1 = Point(self.x1, self.y1)
            point2 = Point(self.x2, self.y1)
            wall = Line(point1, point2)
            self.win.draw_line(wall, fill_colour="#d9d9d9")
        if self.bottom_wall:
            point1 = Point(self.x1, self.y2)
            point2 = Point(self.x2, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall)
        else:
            point1 = Point(self.x1, self.y2)
            point2 = Point(self.x2, self.y2)
            wall = Line(point1, point2)
            self.win.draw_line(wall, fill_colour="#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        colour = "red"
        if undo:
            colour = "gray"
        center1 = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        center2 = Point((to_cell.x1 + to_cell.x2) / 2, (to_cell.y1 + to_cell.y2) / 2)
        line = Line(center1, center2)
        if self.win is None:
            return
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
        win=None,
        seed=None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        if seed:
            random.seed(seed)
        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        self.reset_visited()

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
        if self.win is None:
            return
        cell.draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        self.win.redraw()
        sleep(0.02)

    def break_entrance_and_exit(self):
        self.cells[0][0].top_wall = False
        self.draw_cell(0, 0)
        self.cells[self.num_cols - 1][self.num_rows - 1].bottom_wall = False
        self.draw_cell(self.num_cols - 1, self.num_rows - 1)

    def break_walls_r(self, i, j):
        cell = self.cells[i][j]
        cell.visited = True
        while True:
            to_visit = []
            if (i-1)>=0 and not self.cells[i-1][j].visited:
                to_visit.append((i-1, j))
            if (i+1)<self.num_cols and not self.cells[i+1][j].visited:
                to_visit.append((i+1, j))
            if (j-1)>=0 and not self.cells[i][j-1].visited:
                to_visit.append((i, j-1))
            if (j+1)<self.num_rows and not self.cells[i][j+1].visited:
                to_visit.append((i, j+1))
            if not to_visit:
                self.draw_cell(i, j)
                return
            next_cell = random.randrange(len(to_visit))
            next_i, next_j = to_visit[next_cell]
            if next_i < i:
                cell.left_wall = False
                self.cells[next_i][next_j].right_wall = False
            elif next_i > i:
                cell.right_wall = False
                self.cells[next_i][next_j].left_wall = False
            elif next_j < j:
                cell.top_wall = False
                self.cells[next_i][next_j].bottom_wall = False
            elif next_j > j:
                cell.bottom_wall = False
                self.cells[next_i][next_j].top_wall = False
            self.draw_cell(i, j)
            self.draw_cell(next_i, next_j)
            self.break_walls_r(next_i, next_j)

    def reset_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self.solve_r(0, 0)

    def solve_r(self, i, j):
        self.animate()
        cell = self.cells[i][j]
        cell.visited = True
        if cell == self.cells[self.num_cols - 1][self.num_rows - 1]:
            return True
        directions = [
            (-1, 0, "left"),  # Left
            (1, 0, "right"),   # Right
            (0, -1, "top"),  # Up
            (0, 1, "bottom")    # Down
        ]
        for dir in directions:
            next_i = i + dir[0]
            next_j = j + dir[1]
            if (0 <= next_i < self.num_cols and
                0 <= next_j < self.num_rows and
                not self.cells[next_i][next_j].visited and
                not cell.__dict__[dir[2] + "_wall"]
                ):
                cell.draw_move(self.cells[next_i][next_j])
                if self.solve_r(next_i, next_j):
                    return True
                cell.draw_move(self.cells[next_i][next_j], undo=True)
        return False