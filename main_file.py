import pygame
import random
import tkinter as tk


class GUI:
    def __init__(self, master):
        master.title("GUI")

        tk.Label(master, text="Settings").grid(row=0, columnspan=2)

        # RULES
        overpop_label = tk.Label(master, text="A cell is overpopulated with more than X alive neighbours.")
        overpop_label.grid(row=1, column=0, sticky=tk.W)
        self.overpop_entry = tk.StringVar()
        overpop = tk.Entry(master, textvariable=self.overpop_entry, justify=tk.RIGHT)
        overpop.insert(0, 3)
        overpop.grid(row=1, column=1)

        underpop_label = tk.Label(master, text="A cell is underpopulated with less than X alive neighbours.")
        underpop_label.grid(row=2, column=0, sticky=tk.W)
        self.underpop_entry = tk.StringVar()
        underpop = tk.Entry(master, textvariable=self.underpop_entry, justify=tk.RIGHT)
        underpop.insert(0, 2)
        underpop.grid(row=2, column=1)

        birth_label = tk.Label(master, text="A dead cell with X alive neighbours comes back to live.")
        birth_label.grid(row=3, column=0, sticky=tk.W)
        self.birth_entry = tk.StringVar()
        birth = tk.Entry(master, textvariable=self.birth_entry, justify=tk.RIGHT)
        birth.insert(0, 3)
        birth.grid(row=3, column=1)

        # GRAPHIC SETTINGS
        tk.Label(master, text="Graphic settings").grid(row=4, columnspan=2)

        window_width_label = tk.Label(master, text="How wide do you want the window in pixels?")
        window_width_label.grid(row=5, column=0, sticky=tk.W)
        self.window_size_width = tk.StringVar()
        window_size_width = tk.Entry(master, textvariable=self.window_size_width, justify=tk.RIGHT)
        window_size_width.insert(0, 640)
        window_size_width.grid(row=5, column=1)

        window_height_label = tk.Label(master, text="How high do you want the window in pixels?")
        window_height_label.grid(row=6, column=0, sticky=tk.W)
        self.window_size_height = tk.StringVar()
        window_size_height = tk.Entry(master, textvariable=self.window_size_height, justify=tk.RIGHT)
        window_size_height.insert(0, 480)
        window_size_height.grid(row=6, column=1)

        cell_size_label = tk.Label(master, text="How big do you want the cells in pixels")
        cell_size_label.grid(row=7, column=0, sticky=tk.W)
        self.cell_size_entry = tk.StringVar()
        cell_size_entry = tk.Entry(master, textvariable=self.cell_size_entry, justify=tk.RIGHT)
        cell_size_entry.insert(0, 5)
        cell_size_entry.grid(row=7, column=1)

        # SAVE SETTINGS
        save_button = tk.Button(master, text="Save settings", command=self.clicked)
        save_button.grid(row=10, column=1)

        # GAME BUTTONS
        start_button = tk.Button(master, text="Start", command=self.game_start)
        start_button.grid(row=11, column=1)

        stop_button = tk.Button(master, text="Stop", command=self.game_stop)
        stop_button.grid(row=11, column=2)

    def clicked(self):
        self.overpop_value = self.overpop_entry.get()
        self.underpop_value = self.underpop_entry.get()
        self.birth_value = self.birth_entry.get()
        self.width = self.window_size_width.get()
        self.height = self.window_size_height.get()
        self.cell_size = self.cell_size_entry.get()

    def game_start(self):
        game = LifeGame()
        game.run()

    def game_stop(self):
        game = LifeGame()
        game.game_over = True





dead = 0, 0, 0
alive = 0, 255, 255
fps = 10


class LifeGame:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((int(my_gui.width), int(my_gui.height)))
        self.clear_screen()
        pygame.display.flip()

        self.last_update_completed = 0
        self.ms_between_updates = (1.0 / fps) * 1000.0

        self.active_grid = 0
        self.grids = []
        self.num_cols = int(int(my_gui.width) / int(my_gui.cell_size))
        self.num_rows = int(int(my_gui.height) / int(my_gui.cell_size))
        self.init_grids()
        self.set_grid()

        self.paused = False
        self.game_over = False

    def init_grids(self):

        def create_grid():
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows

        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value = None):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = value
                self.grids[self.active_grid][r][c] = cell_value

    def draw_grid(self):
        self.clear_screen()
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if self.grids[self.active_grid][row][col] == 1:
                    color = alive
                else:
                    color = dead
                pygame.draw.rect(self.screen, color, [int(col * int(my_gui.cell_size)),
                                                      int(row * int(my_gui.cell_size)),
                                                      int(my_gui.cell_size),
                                                      int(my_gui.cell_size)], 0)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(dead)

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

        if self.grids[self.active_grid][row_index][col_index] == 1: # alive
            if num_alive_neighbors > 3:  # overpopulation
                return 0
            if num_alive_neighbors < 2:  # underpopulation
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0: # dead
            if num_alive_neighbors == 3:  # birth
                return 1

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        # inspect active grid and update inactive grid
        # store next iteration and swap with active
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                next_gen_state = self.check_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        return (self.active_grid + 1) % 2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == 's':
                    print("Pause")
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                elif event.unicode == 'r':
                    print("Randomize grid")
                    self.active_grid = 0
                    self.set_grid(None)
                    self.draw_grid()
                elif event.unicode == 'q':
                    print("exit")
                    self.game_over = True


    def run(self):
        while True:
            if self.game_over == True:
                return
            self.handle_events()
            if self.paused:
                continue
            self.update_generation()
            self.draw_grid()
            self.cap_frame_rate()
            # pygame.time.wait(300)

    def cap_frame_rate(self):
        now = pygame.time.get_ticks()
        ms_since_last_update = now - self.last_update_completed
        time_sleep = self.ms_between_updates - ms_since_last_update
        if time_sleep > 0:
           pygame.time.delay(int(time_sleep))
        self.last_update_completed = now



if __name__ == "__main__":
    root = tk.Tk()
    my_gui = GUI(root)
    root.mainloop()

    rule1 = int(my_gui.overpop_value)
    rule2 = int(my_gui.underpop_value)
    rule3 = int(my_gui.birth_value)
    game_size = width, height = int(my_gui.width), int(my_gui.height)
    cell_size = int(my_gui.cell_size)





