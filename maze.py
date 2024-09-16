import time
import random


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
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(
            x1,
            y1,
            x2,
            y2,
        )
        self._animate()

    def _animate(self):
        if self._win is None:
            return

        self._win.redraw()
        time.sleep(0.02)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        cur_cell = self._cells[i][j]
        cur_cell.visited = True

        while True:
            to_visit_index = []

            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit_index.append((i - 1, j))

            if i < len(self._cells) - 1 and not self._cells[i + 1][j].visited:
                to_visit_index.append((i + 1, j))

            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit_index.append((i, j - 1))

            if j < len(self._cells[0]) - 1 and not self._cells[i][j + 1].visited:
                to_visit_index.append((i, j + 1))

            if len(to_visit_index) == 0:
                self._draw_cell(i, j)
                return

            random_direction = random.randrange(len(to_visit_index))
            next_index = to_visit_index[random_direction]
            next_cell = self._cells[next_index[0]][next_index[1]]

            if next_index[0] > i:
                cur_cell.has_right_wall = False
                next_cell.has_left_wall = False
            elif next_index[0] < i:
                cur_cell.has_left_wall = False
                next_cell.has_right_wall = False

            if next_index[1] > j:
                cur_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            elif next_index[1] < j:
                cur_cell.has_top_wall = False
                next_cell.has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

        print("Reset visited cells")

    def _solve_r(self, i, j):
        self._animate()

        cur_cel = self._cells[i][j]
        cur_cel.visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        if (
            i > 0
            and not self._cells[i - 1][j].visited
            and not self._cells[i - 1][j].has_right_wall
        ):
            cur_cel.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                cur_cel.draw_move(self._cells[i - 1][j], True)

        if (
            i < len(self._cells) - 1
            and not self._cells[i + 1][j].visited
            and not self._cells[i + 1][j].has_left_wall
        ):
            cur_cel.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                cur_cel.draw_move(self._cells[i + 1][j], True)

        if (
            j > 0
            and not self._cells[i][j - 1].visited
            and not self._cells[i][j - 1].has_bottom_wall
        ):
            cur_cel.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                cur_cel.draw_move(self._cells[i][j - 1], True)

        if (
            j < len(self._cells[0]) - 1
            and not self._cells[i][j + 1].visited
            and not self._cells[i][j + 1].has_top_wall
        ):
            cur_cel.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                cur_cel.draw_move(self._cells[i][j + 1], True)

        return False

    def solve(self):
        return self._solve_r(0, 0)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)


class Cell:
    def __init__(
        self,
        win,
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
    ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        if self.has_left_wall:
            left_line = Line(self._x1, self._y1, self._x1, self._y2)
            self._win.draw_line(left_line, "red")
        elif not self.has_left_wall:
            left_line = Line(self._x1, self._y1, self._x1, self._y2)
            self._win.draw_line(left_line, "white")

        if self.has_right_wall:
            right_line = Line(self._x2, self._y1, self._x2, self._y2)
            self._win.draw_line(right_line, "red")
        elif not self.has_right_wall:
            right_line = Line(self._x2, self._y1, self._x2, self._y2)
            self._win.draw_line(right_line, "white")

        if self.has_top_wall:
            top_wall = Line(self._x1, self._y1, self._x2, self._y1)
            self._win.draw_line(top_wall, "red")
        elif not self.has_top_wall:
            top_wall = Line(self._x1, self._y1, self._x2, self._y1)
            self._win.draw_line(top_wall, "white")

        if self.has_bottom_wall:
            bottom_wall = Line(self._x1, self._y2, self._x2, self._y2)
            self._win.draw_line(bottom_wall, "red")
        elif not self.has_bottom_wall:
            bottom_wall = Line(self._x1, self._y2, self._x2, self._y2)
            self._win.draw_line(bottom_wall, "white")

    def draw_move(self, to_cell, undo=False):
        line_color = "red"

        if undo:
            line_color = "white"

        half_length = abs(self._x2 - self._x1) // 2
        x_center = half_length + self._x1
        y_center = half_length + self._y1

        half_length2 = abs(to_cell._x2 - to_cell._x1) // 2
        x_center2 = half_length2 + to_cell._x1
        y_center2 = half_length2 + to_cell._y1
        line_between = Line(
            x_center,
            y_center,
            x_center2,
            y_center2,
        )
        self._win.draw_line(line_between, line_color)
