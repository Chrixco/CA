import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Grid dimensions
width, height = 800, 600
cell_size = 10

# Calculate number of cells in each direction
cols, rows = width // cell_size, height // cell_size

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cellular Automaton")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a 2D array to store the state of each cell
grid = np.zeros((rows, cols), dtype=int)

# Function to draw the grid
def draw_grid():
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK if grid[y][x] else WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Function to toggle the state of a cell
def toggle_cell(pos, state):
    x, y = pos[0] // cell_size, pos[1] // cell_size
    if 0 <= x < cols and 0 <= y < rows:  # Check if the position is within bounds
        grid[y][x] = state

# Function to apply the Game of Life rules
def apply_game_of_life_rules():
    new_grid = np.zeros((rows, cols), dtype=int)
    for y in range(rows):
        for x in range(cols):
            # Count the live neighbors
            live_neighbors = sum([grid[y + i][x + j] for i in (-1, 0, 1) for j in (-1, 0, 1) if (i != 0 or j != 0) and (0 <= y + i < rows) and (0 <= x + j < cols)])
            
            # Apply the rules of the Game of Life
            if grid[y][x] == 1 and live_neighbors < 2 or live_neighbors > 3:
                new_grid[y][x] = 0  # Die
            elif grid[y][x] == 0 and live_neighbors == 3:
                new_grid[y][x] = 1  # Come to life
            else:
                new_grid[y][x] = grid[y][x]  # Stay the same
    return new_grid

# Main loop
running = True
paused = True
drawing = False  # Variable to track if the mouse is being dragged
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True  # Start drawing when the mouse button is pressed
            toggle_cell(pygame.mouse.get_pos(), 1)
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False  # Stop drawing when the mouse button is released
        elif event.type == pygame.MOUSEMOTION:
            if drawing:  # If we're currently drawing, toggle cells as the mouse moves
                toggle_cell(pygame.mouse.get_pos(), 1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:  # Reset the game when 'r' is pressed
                grid = np.zeros((rows, cols), dtype=int)

    screen.fill(WHITE)

    if not paused:
        grid = apply_game_of_life_rules()

    draw_grid()
    pygame.display.flip()
    clock.tick(30)  # Increase the clock tick if the drawing feels unresponsive

pygame.quit()
