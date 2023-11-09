import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Grid dimensions
width, height = 800, 600
cell_size = 10
button_height = 40  # Height for the buttons

# Calculate number of cells in each direction
cols, rows = width // cell_size, (height - button_height) // cell_size

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Modified Game of Life")

# Create a 2D array to store the state of each cell
grid = np.zeros((rows, cols), dtype=int)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Module types mapped to integers
module_types = {
    'green': 1,
    'living': 2,
    'commerce': 3,
    'health': 4
}
current_module = 'green'

# Colors for each module type
module_colors = {
    'green': GREEN,
    'living': RED,
    'commerce': BLUE,
    'health': YELLOW
}

# Function to draw the grid
def draw_grid():
    for y in range(rows):
        for x in range(cols):
            color = WHITE
            if grid[y][x] != 0:  # If the cell is not dead, get its color
                for module, value in module_types.items():
                    if grid[y][x] == value:
                        color = module_colors[module]
                        break
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


# Function to draw buttons
def draw_buttons():
    for i, module in enumerate(module_types):
        rect = pygame.Rect(i * (width // len(module_types)), height - button_height, width // len(module_types), button_height)
        pygame.draw.rect(screen, module_colors[module], rect)  # Use module_colors instead of module_types
        pygame.draw.rect(screen, BLACK, rect, 1)

# Function to toggle the state of a cell
def toggle_cell(pos, module):
    x, y = pos[0] // cell_size, pos[1] // cell_size
    if 0 <= x < cols and 0 <= y < rows:  # Check if the position is within bounds
        grid[y][x] = module_types[module]  # Use module_types to get the integer value



def apply_modified_rules():
    new_grid = np.zeros((rows, cols), dtype=int)
    for y in range(rows):
        for x in range(cols):
            # Count the neighbors for each type
            neighbors = {module: 0 for module in module_types}
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i == 0 and j == 0:
                        continue
                    ny, nx = y + i, x + j
                    if 0 <= ny < rows and 0 <= nx < cols:
                        neighbor_type = grid[ny][nx]
                        for module, value in module_types.items():
                            if neighbor_type == value:
                                neighbors[module] += 1

            # Apply the rules based on the current cell's type and its neighbors
            if grid[y][x] == module_types['green']:
                # Green stays if it has 2 or 3 neighbors of any type
                if 2 <= sum(neighbors.values()) <= 3:
                    new_grid[y][x] = module_types['green']
            elif grid[y][x] == module_types['living']:
                # Living stays if it has 2 or 3 living neighbors, otherwise becomes green
                if 2 <= neighbors['living'] <= 3:
                    new_grid[y][x] = module_types['living']
                else:
                    new_grid[y][x] = module_types['green']
            elif grid[y][x] == module_types['commerce']:
                # Commerce becomes or stays alive if it has at least one living neighbor
                if neighbors['living'] >= 1:
                    new_grid[y][x] = module_types['commerce']
            elif grid[y][x] == module_types['health']:
                # Health becomes or stays alive if there are at least two living neighbors
                if neighbors['living'] >= 2:
                    new_grid[y][x] = module_types['health']
            else:
                # If the cell is dead, check for revival conditions
                if neighbors['living'] == 3:
                    new_grid[y][x] = module_types['living']
                elif neighbors['commerce'] >= 1 and neighbors['living'] >= 1:
                    new_grid[y][x] = module_types['commerce']
                elif neighbors['health'] >= 1 and neighbors['living'] >= 2:
                    new_grid[y][x] = module_types['health']

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
            if event.pos[1] > height - button_height:
                # If the click is on the button area, change the current module
                current_module = list(module_types.keys())[(event.pos[0] // (width // len(module_types)))]
            else:
                drawing = True  # Start drawing when the mouse button is pressed
                toggle_cell(event.pos, current_module)
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False  # Stop drawing when the mouse button is released
        elif event.type == pygame.MOUSEMOTION:
            if drawing:  # If we're currently drawing, toggle cells as the mouse moves
                toggle_cell(event.pos, current_module)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:  # Reset the game when 'r' is pressed
                grid = np.zeros((rows, cols), dtype=int)

    screen.fill(WHITE)

    if not paused:
        grid = apply_modified_rules()

    draw_grid()
    draw_buttons()
    pygame.display.flip()
    clock.tick(30)  # Increase the clock tick if the drawing feels unresponsive

pygame.quit()
