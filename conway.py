"""testing for conway's game of life"""
import numpy as np
import pygame

class GameGrid:
    """Class that handles the game's grid."""
    def __init__(self, size):
        self.size = size
        self.grid = self.make_grid(self.size)

    def make_grid(self, size):
        """Creates a two-dimensional array of the specified
        size where all values are the boolean False."""
        gridlist = []
        for glist_i in range(size):
            sublist = []
            for glist_j in range(size):
                sublist.append(False)
            gridlist.append(sublist)
        del glist_i, glist_j
        return np.array(gridlist)

    def count_neighbors(self, row, col):
        """Counts the neighbors of a cell in the grid."""
        neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    val = self.grid[row + i][col + j]
                    if val and not (i == 0 and j == 0):
                        neighbors += 1
                except IndexError:
                    pass
        return neighbors

    def check_cell(self, row, col):
        """Function that determines whether a cell lives or dies in Conway's Game of Life.

        Any cell with three neighbors lives or comes to life.
        Any alive cell with two neighbors survives.
        All other cells die or remain dead. """
        neighbors_alive = self.count_neighbors(row, col)
        cell_living = self.grid[row][col]

        if neighbors_alive == 3:
            return True
        elif cell_living and neighbors_alive == 2:
            return True
        else:
            return False

    def step(self):
        """Performs one step of the game, changing all grid
        values according to the rules of Conway's Game"""
        copy_grid = self.make_grid(self.size)
        for i in range(self.size):
            for j in range(self.size):
                copy_grid[i][j] = self.check_cell(i, j)
        self.grid = copy_grid
        del copy_grid

class GameState:
    """Handles the state of the game and manages
    common variables."""
    def __init__(self, size, grid_px):
        self.size = size
        self.grid_px = grid_px
        self.game = GameGrid(self.size)
        self.startup_running = True
        self.game_running = True
        #the size of the window will allow exactly enough space for all grid spaces
        display_size = self.grid_px * self.size
        self.window = pygame.display.set_mode((display_size, display_size))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()

    def setup_loop(self):
        """Handles the setup phase, where the initial board is set up."""
        print("Click to put down living cells.")
        print("Press space to end the setup phase and run the simulation!")
        while self.startup_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.startup_running = False
                    self.game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    indices = self.pos_to_indices(pygame.mouse.get_pos())
                    row = indices[0]
                    col = indices[1]
                    self.game.grid[row][col] = not self.game.grid[row][col]
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.startup_running = False
            self.render()
            self.clock.tick(10)

    def pos_to_indices(self, mouse_pos):
        """used inside setup_loop to map the mouse's position to the proper grid spot"""
        i_index = int(mouse_pos[1]/self.grid_px)
        j_index = int(mouse_pos[0]/self.grid_px)
        return (i_index, j_index)

    def game_loop(self):
        """Handles the game loop"""
        print("Enjoy! Press Escape to exit!")
        while self.game_running:
            self.game.step()
            #print(self.game.grid)
            self.handle_events()
            self.render()
            self.clock.tick(5)

    def handle_events(self):
        """Handles events for the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    self.game_running = False


    def render(self):
        """Uses pygame to render the game as a grid of white and black squares."""
        #each square should be 10x10px
        for i in range(self.size):
            for j in range(self.size):
                color = (0, 0, 0)
                rect = (self.grid_px * j, self.grid_px * i, self.grid_px, self.grid_px)
                if self.game.grid[i][j]:
                    color = (255, 255, 255)
                pygame.draw.rect(self.window, color, rect)
        pygame.display.update()

pygame.init()
grid_size = int(input("What size grid would you like? [Ans]x[Ans]: "))
game_handler = GameState(grid_size, 10)
game_handler.render()
game_handler.setup_loop()
game_handler.game_loop()
pygame.display.quit()
pygame.quit()
