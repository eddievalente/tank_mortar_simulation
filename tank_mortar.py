import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Mortar Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 36)

# Gravity constant
g = 9.8

# Input boxes and buttons
angle_input = pygame.Rect(50, 50, 140, 32)
speed_input = pygame.Rect(50, 100, 140, 32)
fire_button = pygame.Rect(50, 150, 100, 40)
reset_button = pygame.Rect(50, 200, 100, 40)

angle_text = '45'
speed_text = '50'

# Function to calculate the position of the mortar shell
def calculate_position(angle, speed, time, initial_position):
    rad_angle = math.radians(angle)
    x = initial_position[0] + speed * math.cos(rad_angle) * time
    y = initial_position[1] - (speed * math.sin(rad_angle) * time - 0.5 * g * time ** 2)
    return x, y

# Function to check collision with the target
def check_collision(shell_pos, target_pos, target_radius):
    distance = math.sqrt((shell_pos[0] - target_pos[0]) ** 2 + (shell_pos[1] - target_pos[1]) ** 2)
    return distance <= target_radius

# Draw tank, target, and UI elements
def draw_scene(tank_position, target_position, target_radius, angle_text, speed_text):
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (tank_position[0] - 20, tank_position[1] - 10, 40, 20))  # Tank
    pygame.draw.circle(screen, RED, target_position, target_radius)  # Target

    # Draw input boxes and buttons
    pygame.draw.rect(screen, GRAY, angle_input, 2)
    pygame.draw.rect(screen, GRAY, speed_input, 2)
    pygame.draw.rect(screen, GRAY, fire_button)
    pygame.draw.rect(screen, GRAY, reset_button)

    # Render text
    angle_surface = font.render(angle_text, True, BLACK)
    speed_surface = font.render(speed_text, True, BLACK)
    fire_text = font.render("Fire", True, BLACK)
    reset_text = font.render("Reset", True, BLACK)

    # Blit text
    screen.blit(angle_surface, (angle_input.x + 5, angle_input.y + 5))
    screen.blit(speed_surface, (speed_input.x + 5, speed_input.y + 5))
    screen.blit(fire_text, (fire_button.x + 10, fire_button.y + 5))
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 5))

    pygame.display.flip()

# Main simulation function
def simulate(tank_position, angle, speed, target_position):
    clock = pygame.time.Clock()
    target_radius = 15

    # Initial shell position
    shell_pos = list(tank_position)
    time = 0
    hit = False

    while not hit and shell_pos[1] < HEIGHT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Update shell position
        shell_pos = calculate_position(angle, speed, time, tank_position)
        
        # Draw the scene
        draw_scene(tank_position, target_position, target_radius, angle_text, speed_text)
        
        # Draw the shell
        if 0 <= shell_pos[0] < WIDTH and shell_pos[1] < HEIGHT:
            pygame.draw.circle(screen, BLACK, (int(shell_pos[0]), int(shell_pos[1])), 5)

        # Check for collision with target
        hit = check_collision(shell_pos, target_position, target_radius)

        # Update display and time
        pygame.display.flip()
        time += 0.1
        clock.tick(60)

    # Display result
    if hit:
        print(f"Angle: {angle}, Speed: {speed} m/s. Result: Target hit!")
    else:
        print(f"Angle: {angle}, Speed: {speed} m/s. Result: Missed the target!")

    pygame.time.wait(2000)

# Parameters for simulation
def main():
    global angle_text, speed_text

    tank_position = (100, 550)  # Tank position (x, y)
    target_position = (700, 550)  # Target position (x, y)
    target_radius = 15

    running = True
    firing = False
    angle = 0
    speed = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if fire_button.collidepoint(event.pos):
                    try:
                        angle = float(angle_text)
                        speed = float(speed_text)
                        firing = True
                    except ValueError:
                        print("Invalid input. Please enter numbers for angle and speed.")

                if reset_button.collidepoint(event.pos):
                    angle_text = ''
                    speed_text = ''
                    firing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if angle_input.collidepoint(pygame.mouse.get_pos()):
                        angle_text = angle_text[:-1]
                    elif speed_input.collidepoint(pygame.mouse.get_pos()):
                        speed_text = speed_text[:-1]
                else:
                    if angle_input.collidepoint(pygame.mouse.get_pos()):
                        angle_text += event.unicode
                    elif speed_input.collidepoint(pygame.mouse.get_pos()):
                        speed_text += event.unicode

        draw_scene(tank_position, target_position, target_radius, angle_text, speed_text)

        if firing:
            simulate(tank_position, angle, speed, target_position)
            firing = False

    pygame.quit()

if __name__ == "__main__":
    main()
