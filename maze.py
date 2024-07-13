from cell import Cell
import random

from graphics import Window


class MazeManager:
    def __init__(self, window: Window, screen_x, screen_y):
        self.window = window
        self.maze = None
        self.screen_x = screen_x
        self.screen_y = screen_y

        # Add buttons to the window for generating and solving the maze
        window.create_button("Generate Maze", self.generate_maze, "left", "nw")
        window.create_button("Solve Maze", self.solve_maze, "left", "nw")

    def generate_maze(self):
        try:
            num_rows = int(self.window.get_entry_value("Rows"))
            num_cols = int(self.window.get_entry_value("Columns"))

            if not (1 <= num_rows <= 100):
                self.window.create_mb("Error", "Rows must be between 1 and 100")
                return

            if not (1 <= num_cols <= 100):
                self.window.create_mb("Error", "Columns must be between 1 and 100")
                return

            margin = 50

            cell_size_x = (self.screen_x - 2 * margin) / num_cols
            cell_size_y = (self.screen_y - 2 * margin) / num_rows

            # Clear previous maze
            self.window.clear_canvas()

            self.maze = Maze(
                margin,
                margin,
                num_rows,
                num_cols,
                cell_size_x,
                cell_size_y,
                self.window,
            )
            self.maze.create_cells()
            self.maze.create_maze()

        except ValueError:
            self.window.create_mb(
                "Error", "Please enter valid numbers for rows and columns"
            )

    def solve_maze(self):
        if self.maze:
            if self.maze.solve():
                self.window.create_mb("Winner", "Winner")
            else:
                self.window.create_mb("No Solution", "No Solution Found")
        else:
            self.window.create_mb("Error", "No Maze to Solve")


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

    def create_cells(self):
        self._create_cells()
        self._break_entrance_and_exit()

    def create_maze(self):
        self.row_limit = 35
        self.col_limit = 45

        if self._num_rows < self.row_limit and self._num_cols < self.col_limit:
            self._break_walls_r(0, 0)
        else:
            self._break_walls()

        self._reset_cells_visited()

    ############### CREATE CELLS #################
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    ################### CREATE RANDOM MAZE #######################
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right, i < self_num_cols -1 ensures its not on the rightmost edge of the maze.
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _break_walls(self):
        stack = [(0, 0)]
        self._cells[0][0].visited = True

        while stack:
            i, j = stack[-1]
            neighbors = []

            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                neighbors.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                neighbors.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                neighbors.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                neighbors.append((i, j + 1))

            if neighbors:
                next_i, next_j = random.choice(neighbors)

                # knock out walls between this cell and the next cell(s)
                # right
                if next_i == i + 1:
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_i][next_j].has_left_wall = False
                # left
                if next_i == i - 1:
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_i][next_j].has_right_wall = False
                # down
                if next_j == j + 1:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_i][next_j].has_top_wall = False
                # up
                if next_j == j - 1:
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_i][next_j].has_bottom_wall = False

                self._cells[next_i][next_j].visited = True
                stack.append((next_i, next_j))
            else:
                self._draw_cell(i, j)
                stack.pop()

    ################## SOLVE ################################
    def solve(self):
        i = 0
        j = 0

        if self._num_rows < self.row_limit and self._num_cols < self.col_limit:
            if self._solve_r(i, j):
                return True
            else:
                return False
        else:
            if self._solve():
                return True
            else:
                return False

    def _solve(self):
        """
        Iterative DFS search
        """

        self._animate()
        stack = [(0, 0)]
        self._cells[0][0].visited = True

        while stack:
            i, j = stack[-1]
            if (i, j) == (self._num_cols - 1, self._num_rows - 1):
                return True

            # valid neighbor
            neighbors = []

            # left
            if (
                i > 0
                and not self._cells[i - 1][j].visited
                and not self._cells[i][j].has_left_wall
            ):
                neighbors.append((i - 1, j))

            # right
            if (
                i < self._num_cols - 1
                and not self._cells[i + 1][j].visited
                and not self._cells[i][j].has_right_wall
            ):
                neighbors.append((i + 1, j))

            # up
            if (
                j > 0
                and not self._cells[i][j - 1].visited
                and not self._cells[i][j].has_top_wall
            ):
                neighbors.append((i, j - 1))

            # down
            if (
                j < self._num_rows - 1
                and not self._cells[i][j + 1].visited
                and not self._cells[i][j].has_bottom_wall
            ):
                neighbors.append((i, j + 1))

            if neighbors:
                next_i, next_j = neighbors[0]
                self._cells[next_i][next_j].visited = True
                self._cells[i][j].draw_move(self._cells[next_i][next_j])
                stack.append((next_i, next_j))

            else:
                stack.pop()
                if stack:
                    prev_i, prev_j = stack[-1]
                    self._cells[i][j].draw_move(self._cells[prev_i][prev_j], undo=True)

            self._animate()

        return False

    def _solve_r(self, i, j):
        """
        Recursive DFS search
        """
        self._animate()
        self._cells[i][j].visited = True

        if self._cells[i][j] == self._cells[-1][-1]:
            return True
        # left
        if (
            i > 0
            and not self._cells[i - 1][j].visited
            and not self._cells[i][j].has_left_wall
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)
        # right
        if (
            i < self._num_cols - 1
            and not self._cells[i + 1][j].visited
            and not self._cells[i][j].has_right_wall
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)
        # up
        if (
            j > 0
            and not self._cells[i][j - 1].visited
            and not self._cells[i][j].has_top_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        # down
        if (
            j < self._num_rows - 1
            and not self._cells[i][j + 1].visited
            and not self._cells[i][j].has_bottom_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)
        return False

    ########## UTILS ################
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        # time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _reset_cells_visited(self):
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._cells[col][row].visited = False
                print(self._cells[col][row])
