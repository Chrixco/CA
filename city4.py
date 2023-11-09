import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Grid dimensions
width, height = 800, 600
cell_size = 40
button_height = 40  # Height for the buttons

# Calculate number of cells in each direction
cols, rows = width // cell_size, (height - button_height) // cell_size

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Modified Game of Life")

# Create a 2D array to store the state of each cell and their entropy
grid = np.zeros((rows, cols), dtype=int)
entropy_grid = np.zeros((rows, cols))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)  # Define purple for healthcare facilities

#Default entropy
default_entropy_value = 30

# Module types mapped to integers
module_types = {
    'green': 1,       # Green spaces
    'formal': 2,      # Formal structures
    'informal': 3,    # Informal structures
    'commerce': 4,    # Commercial areas
    'health': 5       # Healthcare facilities
}

# Entropy values for each module type
entropy_values = {
    'green': 30,       # Green spaces have moderate entropy, they can change but not too rapidly
    'formal': 10,      # Formal structures have very low entropy, indicating stability and order
    'informal': 70,    # Informal structures have high entropy, reflecting their dynamic and unpredictable nature
    'commerce': 50,    # Commercial areas have moderate to high entropy, they can evolve depending on economic factors
    'health': 40       # Healthcare facilities have moderate entropy, they are less likely to change than commercial areas but more than formal structures
}

# Colors for each module type
module_colors = {
    'green': GREEN, 
    'formal': BLUE,
    'informal': RED,
    'commerce': YELLOW,
    'health': PURPLE
}

current_module = 'green'

# Function to draw the grid and display entropy values
def draw_grid(grid, entropy_grid):
    for y in range(rows):
        for x in range(cols):
            color = WHITE
            if grid[y][x] != 0:  # If the cell is not dead, get its color
                module_key = next(key for key, value in module_types.items() if value == grid[y][x])
                color = module_colors[module_key]
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            # Render the entropy value as text
            entropy_value = entropy_grid[y][x]
            font = pygame.font.SysFont(None, 24)  # Choose a font and size that fits your cell size
            text = font.render(f"{entropy_value:.2f}", True, BLACK)  # Render the text with two decimal places
            text_rect = text.get_rect(center=rect.center)  # Center the text in the cell
            screen.blit(text, text_rect)


# Function to draw buttons
def draw_buttons():
    for i, module in enumerate(module_types):
        rect = pygame.Rect(i * (width // len(module_types)), height - button_height, width // len(module_types), button_height)
        pygame.draw.rect(screen, module_colors[module], rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

# Function to toggle the state of a cell
def toggle_cell(pos, module):
    x, y = pos[0] // cell_size, pos[1] // cell_size
    if 0 <= x < cols and 0 <= y < rows:  # Check if the position is within bounds
        grid[y][x] = module_types[module]
        adjust_entropy(y, x, entropy_values[module])

# Helper function to determine if a transition should occur based on entropy
def should_transition(entropy, threshold, influence):
    # The probability of transition increases as the entropy difference increases
    probability = (entropy - threshold + influence) / 2
    return random.random() < probability

# Function to adjust entropy in the grid
def adjust_entropy(y, x, entropy):
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            ny, nx = y + i, x + j
            if 0 <= ny < rows and 0 <= nx < cols:
                entropy_grid[ny][nx] += entropy
                entropy_grid[ny][nx] = min(1, max(0, entropy_grid[ny][nx]))  # Ensure entropy stays between 0 and 1

# Function to apply city rules based on entropy
# Function to apply city rules based on entropy
def apply_city_rules(grid, module_types, entropy_grid, entropy_values, default_entropy_value):
    new_grid = np.zeros((rows, cols), dtype=int)
    new_entropy_grid = np.copy(entropy_grid)  # Copy the current entropy grid to update it

    for y in range(rows):
        for x in range(cols):
            # Calculate the influence of neighboring cells
            entropy_influence = 0
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i == 0 and j == 0:
                        continue
                    ny, nx = y + i, x + j
                    if 0 <= ny < rows and 0 <= nx < cols:
                        entropy_influence += entropy_grid[ny][nx]

            # Normalize the entropy influence
            entropy_influence /= 8  # There are 8 neighbors

            current_type = grid[y][x]
            current_entropy = entropy_grid[y][x]

            # Apply rules based on the current module type and its entropy
            for y in range(rows):
                for x in range(cols):
                    # ... (previous code to calculate entropy_influence)

                    current_type = grid[y][x]
                    current_entropy = entropy_grid[y][x]

                    # Formal structures  may degrade to informal based on entropy and influence
                    if current_type == module_types['formal']:
                        if should_transition(current_entropy, entropy_values['formal'], entropy_influence):
                            new_grid[y][x] = module_types['informal']

                    # Informal structures may upgrade to formal based on entropy and influence
                    elif current_type == module_types['informal']:
                        if should_transition(current_entropy, entropy_values['informal'], -entropy_influence):
                            new_grid[y][x] = module_types['formal']

                    # Green spaces may become informal based on surrounding entropy
                    elif current_type == module_types['green']:
                        if should_transition(entropy_influence, entropy_values['green'], 0):
                            new_grid[y][x] = module_types['informal']

                    # Commercial areas may degrade based on surrounding entropy
                    elif current_type == module_types['commerce']:
                        if should_transition(entropy_influence, entropy_values['commerce'], 0):
                            new_grid[y][x] = module_types['informal']

                    # Healthcare facilities may degrade based on surrounding entropy
                    elif current_type == module_types['health']:
                        if should_transition(entropy_influence, entropy_values['health'], 0):
                            new_grid[y][x] = module_types['informal']

                    # If no transition occurs, maintain current type
                    if new_grid[y][x] == 0:
                        new_grid[y][x] = current_type

            # Calculate the new entropy value based on the type of module placed
            new_entropy_value = entropy_values.get(current_type, default_entropy_value)

            # Adjust the entropy of the current cell
            new_entropy_grid[y][x] = new_entropy_value

            # Adjust the entropy of neighboring cells based on the new entropy value
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i == 0 and j == 0:
                        continue
                    ny, nx = y + i, x + j
                    if 0 <= ny < rows and 0 <= nx < cols:
                        # Update the entropy of neighbors with some factor of the new entropy value
                        entropy_factor = 0.1  # This factor can be adjusted
                        new_entropy_grid[ny][nx] += entropy_factor * new_entropy_value
                        # Ensure entropy stays between 0 and 1
                        new_entropy_grid[ny][nx] = min(1, max(0, new_entropy_grid[ny][nx]))

    return new_grid, new_entropy_grid



# Main loop and event handling...
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
                entropy_grid = np.full((rows, cols), default_entropy_value)

    screen.fill(WHITE)

    if not paused:
     grid, entropy_grid = apply_city_rules(grid, module_types, entropy_grid, entropy_values, default_entropy_value)

    draw_grid(grid, entropy_grid)
    draw_buttons()
    pygame.display.flip()
    clock.tick(60)  # Increase the clock tick if the drawing feels unresponsive

pygame.quit()