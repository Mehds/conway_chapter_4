import time
from cell import Cell

CELL_OFFSET = 2


class Grid:
    def __init__(self, screen_dimensions: tuple, width: int, height: int):
        self.width = width
        self.height = height

        screen_width, screen_height = screen_dimensions
        cell_width, cell_height = (screen_width / (width + 1), screen_height / (height + 1))

        self.cells = [
            [Cell((x * (cell_width + CELL_OFFSET), y * (cell_height + CELL_OFFSET)), (cell_width, cell_height)) for x in range(width)] for y in
            range(height)]
        self.rects = []

    def __str__(self):
        output = ""
        for row in self.cells:
            for cell in row:
                output += str(cell)
            output += "\n"
        return output

    def flip(self, col: int, row: int):
        if col < 0 or col >= self.width:
            raise RuntimeError(
                f"error updating cell at column {col}: expected column number between 0 and {self.width - 1}")
        if row < 0 or row >= self.height:
            raise RuntimeError(
                f"error updating cell at row {row}: expected column number between 0 and {self.height - 1}")

        self.cells[row][col].flip()

    def compute_future_states(self):
        # navigate through the grid, for each cell find its valid neighbors
        for row_index, row in enumerate(self.cells):
            for col_index, cell in enumerate(row):
                cell.set_future_state(self.__count_living_neighbors(col_index, row_index))

    def update(self):
        for row in self.cells:
            for cell in row:
                cell.update()

    def draw(self, surface):
        self.rects = []

        for row in self.cells:
            self.rects.append([cell.draw(surface) for cell in row])

    def check_clicks(self, pos):
        print('checking for collisions')
        for i, row in enumerate(self.rects):
            for j, rect in enumerate(row):
                if rect.collidepoint(pos):
                    print(f'collided with {rect} at pos {i}, {j}')
                    self.cells[i][j].flip()

    # cells have up to 8 neighbours, except cells in the boundary rows and columns.
    # this iterator yields a given position's neighbors
    def __count_living_neighbors(self, col: int, row: int):
        if col < 0 or col >= self.width:
            raise RuntimeError(
                f"error updating cell at column {col}: expected column number between 0 and {self.width - 1}")
        if row < 0 or row >= self.height:
            raise RuntimeError(
                f"error updating cell at row {row}: expected column number between 0 and {self.height - 1}")

        count = 0
        # top left
        if row > 0 and col > 0 and self.cells[row - 1][col - 1].active:
            count += 1
        # top
        if row > 0 and self.cells[row - 1][col].active:
            count += 1
        # top right
        if row > 0 and col < self.width - 1 and self.cells[row - 1][col + 1].active:
            count += 1
        # right
        if col < self.width - 1 and self.cells[row][col + 1].active:
            count += 1
        # bottom right
        if row < self.height - 1 and col < self.width - 1 and self.cells[row + 1][col + 1].active:
            count += 1
        # bottom
        if row < self.height - 1 and col < self.width - 1 and self.cells[row + 1][col].active:
            count += 1
        # bottom left
        if row < self.height - 1 and col < self.width - 1 and self.cells[row + 1][col - 1].active:
            count += 1
        # left
        if col < self.width - 1 and self.cells[row][col - 1].active:
            count += 1

        return count


if __name__ == "__main__":
    g = Grid((200, 200), 10, 10)
    print(g)

    g.flip(2, 1)
    g.flip(3, 2)
    g.flip(1, 3)
    g.flip(2, 3)
    g.flip(3, 3)

    print(g)

    for x in range(15):
        g.compute_future_states()
        g.update()
        print(g)
        time.sleep(1)
