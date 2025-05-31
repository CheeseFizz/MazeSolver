from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

class Window:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

        self.__root = Tk()
        self.__root.minsize(width, height)
        self.__root.maxsize(width, height)
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root, bg="white", height=self.__height, width=self.__width)
        self.__canvas.pack()

        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
            

    def close(self):
        self.running = False
        
class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            window=None,
            seed=None
        ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = window
        self.seed = seed

        if self.seed:
            random.seed(seed)

        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.num_cols):
            temp = []
            for j in range(self.num_rows):
                temp.append(Cell(self.win))
            self.__cells.append(temp)

        # given the direction to animate drawing the cells in the __draw_cell method, I think looping again might be fine?
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        cell_x1 = self.x1 + (i * self.cell_size_x)
        cell_x2 = cell_x1 + self.cell_size_x
        cell_y1 = self.y1 + (j * self.cell_size_y)
        cell_y2 = cell_y1 + self.cell_size_y
        
        self.__cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self.__animate()

    def __animate(self):
        if self.win:
            self.win.redraw()
        sleep(0.015)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        self.__cells[-1][-1].has_bottom_wall = False
        self.__draw_cell(self.num_cols-1, self.num_rows-1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            to_visit = []

            try:
                if not self.__cells[i+1][j].visited:
                    to_visit.append((i+1, j))
            except IndexError:
                pass
            try:
                if not self.__cells[i-1][j].visited and i != 0:
                    to_visit.append((i-1, j))
            except IndexError:
                pass
            try:
                if not self.__cells[i][j+1].visited:
                    to_visit.append((i, j+1))
            except IndexError:
                pass
            try:
                if not self.__cells[i][j-1].visited and j != 0:
                    to_visit.append((i, j-1))
            except IndexError:
                pass

            if len(to_visit) == 0:
                self.__draw_cell(i,j)
                return

            r = random.choice(to_visit)
            #print(f"at {i},{j}: next choice {r[0]},{r[1]}")

            if r[0] - i == 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[r[0]][r[1]].has_left_wall = False
            elif r[0] - i == -1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[r[0]][r[1]].has_right_wall = False

            if r[1] - j == 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[r[0]][r[1]].has_top_wall = False
            elif r[1] - j == -1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[r[0]][r[1]].has_bottom_wall = False

            self.__draw_cell(i,j)
            self.__draw_cell(r[0],r[1])

            self.__break_walls_r(r[0],r[1])
        

    def __reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__cells[i][j].visited = False


    def solve(self):
        return self.__solve_r(0, 0)

    def __solve_r(self, i, j):
        self.__animate()
        self.__cells[i][j].visited = True
        if i == (self.num_cols - 1) and j == (self.num_rows - 1):
            return True
        try:
            if (
                not self.__cells[i+1][j].visited
                and not self.__cells[i][j].has_right_wall
            ):
                self.__cells[i][j].draw_move(self.__cells[i+1][j])
                if self.__solve_r(i+1, j):
                    return True
                else:
                    self.__cells[i][j].draw_move(self.__cells[i+1][j], undo=True)
        except IndexError:
            pass
        try:
            if (
                not self.__cells[i-1][j].visited
                and not self.__cells[i][j].has_left_wall
            ):
                self.__cells[i][j].draw_move(self.__cells[i-1][j])
                if self.__solve_r(i-1, j):
                    return True
                else:
                    self.__cells[i][j].draw_move(self.__cells[i-1][j], undo=True)
        except IndexError:
            pass
        try:
            if (
                not self.__cells[i][j+1].visited
                and not self.__cells[i][j].has_bottom_wall
            ):
                self.__cells[i][j].draw_move(self.__cells[i][j+1])
                if self.__solve_r(i, j+1):
                    return True
                else:
                    self.__cells[i][j].draw_move(self.__cells[i][j+1], undo=True)
        except IndexError:
            pass
        try:
            if (
                not self.__cells[i][j-1].visited
                and not self.__cells[i][j].has_top_wall
            ):
                self.__cells[i][j].draw_move(self.__cells[i][j-1])
                if self.__solve_r(i, j-1):
                    return True
                else:
                    self.__cells[i][j].draw_move(self.__cells[i][j-1], undo=True)
        except IndexError:
            pass

        return False



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            width = 2,
            fill = fill_color
        )

class Cell:
    def __init__(self, window=None):
        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1
        self.win = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.has_left_wall:
            color = "black"
        else:
            color = "white"
        pl1 = Point(self.__x1, self.__y1)
        pl2 = Point(self.__x1, self.__y2)
        ll1 = Line(pl1, pl2)
        if self.win:
            self.win.draw_line(ll1, color)

        if self.has_right_wall:
            color = "black"
        else:
            color = "white"
        pr1 = Point(self.__x2, self.__y1)
        pr2 = Point(self.__x2, self.__y2)
        lr1 = Line(pr1, pr2)
        if self.win:
            self.win.draw_line(lr1, color)

        if self.has_top_wall:
            color = "black"
        else:
            color = "white"
        pt1 = Point(self.__x1, self.__y1)
        pt2 = Point(self.__x2, self.__y1)
        lt1 = Line(pt1, pt2)
        if self.win:
            self.win.draw_line(lt1, color)
        
        if self.has_bottom_wall:
            color = "black"
        else:
            color = "white"
        pb1 = Point(self.__x1, self.__y2)
        pb2 = Point(self.__x2, self.__y2)
        lb1 = Line(pb1, pb2)
        if self.win:
            self.win.draw_line(lb1, color)

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"
        center = Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)
        to_center = Point((to_cell.__x1 + to_cell.__x2) / 2, (to_cell.__y1 + to_cell.__y2) / 2)
        move_line = Line(center, to_center)
        if self.win:
            self.win.draw_line(move_line, color)
        

