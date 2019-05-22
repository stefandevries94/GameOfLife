import tkinter as tk
import random


class Test(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", expand="true")

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
        self.button_frame = tk.Frame()
        self.button_frame.pack()
        start_button = tk.Button(self.button_frame, text="Start", command=self.run)
        start_button.pack(side="left")

        stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_game)
        stop_button.pack(side="left")

        reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_game)
        reset_button.pack(side="left")

        # GAME RULES
        self.rules_frame = tk.Frame()
        self.rules_frame.pack()

        overpop_label = tk.Label(self.rules_frame, text="A cell is overpopulated with more than X alive neighbours.")
        overpop_label.grid(row=0, column=0)
        self.overpop_entry = tk.StringVar()
        overpop = tk.Entry(self.rules_frame, textvariable=self.overpop_entry, justify=tk.RIGHT, width=2)
        overpop.insert(0, 3)
        overpop.grid(row=0, column=1)

        underpop_label = tk.Label(self.rules_frame, text="A cell is underpopulated with less than X alive neighbours.")
        underpop_label.grid(row=1, column=0)
        self.underpop_entry = tk.StringVar()
        underpop = tk.Entry(self.rules_frame, textvariable=self.underpop_entry, justify=tk.RIGHT, width=2)
        underpop.insert(0, 2)
        underpop.grid(row=1, column=1)

        birth_label = tk.Label(self.rules_frame, text="A dead cell with X alive neighbours comes back to live.")
        birth_label.grid(row=2, column=0)
        self.birth_entry = tk.StringVar()
        birth = tk.Entry(self.rules_frame, textvariable=self.birth_entry, justify=tk.RIGHT, width=2)
        birth.insert(0, 3)
        birth.grid(row=2, column=1)



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