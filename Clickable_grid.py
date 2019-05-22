import tkinter as tk
import random


class Test(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        # GAME SETTINGS
        self.cellwidth = self.cellheight = 10
        print(self.cellwidth)
        self.num_col = int(500 / self.cellwidth)
        self.num_row = int(500 / self.cellheight)
        self.speed = 100


        self.active_grid = 0
        self.grids = []
        self.init_grids()
        # self.set_grid()
        self.draw_canvas()
        self.canvas.bind("<Button-1>", self.callback)

        self.game_over = -1

        # SIMULATION BUTTONS
        start_button = tk.Button(self, text="Start", command=self.run)
        start_button.pack()

        stop_button = tk.Button(self, text="Stop", command=self.stop_game)
        stop_button.pack()

        reset_button = tk.Button(self, text="Reset", command=self.reset_game)
        reset_button.pack()

        # GAME RULES
        overpop_label = tk.Label(self, text="A cell is overpopulated with more than X alive neighbours.")
        overpop_label.pack()
        self.overpop_entry = tk.StringVar()
        overpop = tk.Entry(self, textvariable=self.overpop_entry, justify=tk.RIGHT)
        overpop.insert(0, 3)
        overpop.pack()

        underpop_label = tk.Label(self, text="A cell is underpopulated with less than X alive neighbours.")
        underpop_label.pack()
        self.underpop_entry = tk.StringVar()
        underpop = tk.Entry(self, textvariable=self.underpop_entry, justify=tk.RIGHT)
        underpop.insert(0, 2)
        underpop.pack()

        birth_label = tk.Label(self, text="A dead cell with X alive neighbours comes back to live.")
        birth_label.pack()
        self.birth_entry = tk.StringVar()
        birth = tk.Entry(self, textvariable=self.birth_entry, justify=tk.RIGHT)
        birth.insert(0, 3)
        birth.pack()



    def init_grids(self):
        def create_grid():
            rows = []
            for row_num in range(self.num_row):
                list_of_columns = [0] * self.num_col
                rows.append(list_of_columns)
            return rows

        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value=None):
        for r in range(self.num_row):
            for c in range(self.num_col):
                if value is None:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = value
                self.grids[self.active_grid][r][c] = cell_value

    def draw_canvas(self):
        self.rect = dict()
        for row in range(self.num_row):
            for column in range(self.num_col):
                x1 = row*self.cellheight
                y1 = column * self.cellwidth
                x2 = x1 + self.cellheight
                y2 = y1 + self.cellwidth
                if self.grids[self.active_grid][row][column] == 1:
                    color = "black"
                else:
                    color = "white"
                self.rect[(row,column)] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="rect")

    def callback(self, event):
        col = int(event.x//self.cellwidth)
        row = int(event.y//self.cellheight)
        if not self.grids[self.active_grid][row][col]:
            self.grids[self.active_grid][row][col] = 1
            self.canvas.itemconfig(self.rect[(col, row)], fill="black")
        else:
            self.grids[self.active_grid][row][col] = 0
            self.canvas.itemconfig(self.rect[(col, row)], fill="white")

    def clear_screen(self):
        self.rect = dict()
        for row in range(self.num_row):
            for column in range(self.num_col):
                self.x1 = column * self.cellwidth
                self.y1 = row * self.cellheight
                self.x2 = self.x1 + self.cellwidth
                self.y2 = self.y1 + self.cellheight
                self.rect[(row, column)] = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="white", tags="rect")

    def get_cell(self, r, c):
        try:
            cell_value = self.grids[self.active_grid][r][c]
        except:
            cell_value = 0
        return cell_value

    def check_neighbors(self, row_index, col_index):
        num_alive_neighbors = 0
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)

        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)

        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        if self.grids[self.active_grid][row_index][col_index] == 1:  # alive
            if num_alive_neighbors > int(self.overpop_entry.get()):  # overpopulation
                return 0
            if num_alive_neighbors < int(self.underpop_entry.get()):  # underpopulation
                return 0
            if num_alive_neighbors >= int(self.underpop_entry.get()) and num_alive_neighbors <= int(self.overpop_entry.get()):
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0:  # dead
            if num_alive_neighbors == int(self.birth_entry.get()):  # birth
                return 1

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        for r in range(self.num_row):
            for c in range(self.num_col):
                next_gen_state = self.check_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        return (self.active_grid + 1) % 2

    def stop_game(self):
        self.game_over = self.game_over*-1

    def reset_game(self):
        self.active_grid = 0
        self.init_grids()
        self.set_grid(0)
        # self.draw_canvas()

    def redraw(self, delay):
        if self.game_over == 1:
            print("stopped")
        else:
            for r in range(self.num_row):
                for c in range(self.num_col):
                    if self.grids[self.active_grid][r][c] == 1:
                        color = "black"

                    else:
                        color = "white"
                    self.canvas.itemconfig(self.rect[(c,r)], fill=color)

            self.after(delay, lambda: self.redraw(delay))
            self.update_generation()

    def run(self):
        self.game_over = -1
        self.redraw(self.speed)

if __name__ == "__main__":
    test = Test()
    test.mainloop()