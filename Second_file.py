import tkinter as tk
import random




class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.cellwidth = 10
        self.cellheight = 10
        self.num_col = int(500 / self.cellwidth)
        self.num_row =int(500 / self.cellheight)



        self.clear_screen()

        self.active_grid = 0
        self.grids = []
        self.init_grids()
        self.set_grid()
        self.draw_canvas()

        self.redraw(100)








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
        self.clear_screen()

        for row in range(self.num_row):
            for column in range(self.num_col):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if self.grids[self.active_grid][row][column] == 1:
                    color = "black"
                else:
                    color = "white"
                self.rect[(row,column)] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="rect")

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
            if num_alive_neighbors > 3:  # overpopulation
                return 0
            if num_alive_neighbors < 2:  # underpopulation
                return 0
            if num_alive_neighbors >= 2 and num_alive_neighbors <= 3:
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0:  # dead
            if num_alive_neighbors == 3:  # birth
                return 1

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        # self.set_grid(0)
        for r in range(self.num_row):
            for c in range(self.num_col):
                next_gen_state = self.check_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        return (self.active_grid + 1) % 2

    def redraw(self, delay):

        # self.canvas.itemconfig("rect", fill="white")

        # self.draw_canvas()


        for r in range(self.num_row):
            for c in range(self.num_col):
                if self.grids[self.active_grid][r][c] == 1:
                    color = "black"

                else:
                    color = "white"
                self.canvas.itemconfig(self.rect[(r,c)], fill=color)

        self.after(delay, lambda: self.redraw(delay))
        self.update_generation()






if __name__ == "__main__":
    app = App()
    app.mainloop()


