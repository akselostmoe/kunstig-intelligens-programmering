class HexCell:
    def __init__(self, row, column, size, value):
        self.size = size
        self.value = value
        self.row = row
        self.column = column
        self.placement = (row, column)
        self.neighbors = self.initialize_neighbors_list()

    # initializes neighbors
    def initialize_neighbors_list(self):
        n_list = []
        if self.row - 1 >= 0:
            n_list.append((self.row - 1, self.column))
        if self.row - 1 >= 0 and self.column + 1 < self.size:
            n_list.append((self.row - 1, self.column + 1))
        if self.column + 1 < self.size:
            n_list.append((self.row, self.column + 1))
        if self.row + 1 < self.size:
            n_list.append((self.row + 1, self.column))
        if self.row + 1 < self.size and self.column - 1 >= 0:
            n_list.append((self.row + 1, self.column - 1))
        if self.column - 1 >= 0:
            n_list.append((self.row, self.column - 1))
        return n_list

    def update_cell(self, value):
        self.value = value
