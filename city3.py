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
    'green': 1,       # Green spaces
    'formal': 2,      # Formal structures
    'informal': 3,    # Informal structures
    'commerce': 4,    # Commercial areas
    'health': 5       # Healthcare facilities
}
current_module = 'green'

# Colors for each module type
module_colors = {
    'green': GREEN,       # Green spaces are green
    'formal': BLUE,       # Formal structures are blue
    'informal': RED,      # Informal structures are red
    'commerce': YELLOW,   # Commercial areas are yellow
    'health': YELLOW      # Healthcare facilities are purple (assuming you define PURPLE)
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

def apply_city_rules(grid, module_types):
    new_grid = np.zeros((rows, cols), dtype=int)
    for y in range(rows):
        for x in range(cols):
            neighbors = {module: 0 for module in module_types.values()}  # Use module values for keys
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i == 0 and j == 0:
                        continue
                    ny, nx = y + i, x + j
                    if 0 <= ny < rows and 0 <= nx < cols:
                        neighbor_type = grid[ny][nx]
                        if neighbor_type in neighbors:  # Check if the neighbor_type is a valid key
                            neighbors[neighbor_type] += 1

            current_type = grid[y][x]
            # Formal structures
            if current_type == module_types['formal']:
                if neighbors[module_types['informal']] == 0 and neighbors[module_types['green']] >= 2:
                    new_grid[y][x] = module_types['formal']
                else:
                    new_grid[y][x] = module_types['green']  # Revert to green space if overcrowded

            # Informal structures
            elif current_type == module_types['informal']:
                if neighbors[module_types['formal']] == 0 or neighbors[module_types['green']] >= 1:
                    new_grid[y][x] = module_types['informal']
                else:
                    new_grid[y][x] = module_types['formal']  # Become formal if surrounded by formal structures

            # Green spaces
            elif current_type == module_types['green']:
                if neighbors[module_types['informal']] > neighbors[module_types['formal']]:
                    new_grid[y][x] = module_types['informal']  # Overtaken by informal structures
                else:
                    new_grid[y][x] = module_types['green']  # Remain as green space

            # Commerce and health
            elif current_type in [module_types['commerce'], module_types['health']]:
                if neighbors[module_types['formal']] > neighbors[module_types['informal']]:
                    new_grid[y][x] = current_type  # Stay the same if supported by formal structures
                else:
                    new_grid[y][x] = module_types['informal']  # Become informal if not supported

            # Empty cells
            else:
                if neighbors[module_types['informal']] > neighbors[module_types['formal']]:
                    new_grid[y][x] = module_types['informal']  # Develop into informal if isolated
                elif neighbors[module_types['formal']] >= 3:
                    new_grid[y][x] = module_types['formal']  # Develop into formal if supported

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
        grid = apply_city_rules(grid, module_types)

    draw_grid()
    draw_buttons()
    pygame.display.flip()
    clock.tick(30)  # Increase the clock tick if the drawing feels unresponsive

pygame.quit()
