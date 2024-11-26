import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Load the track image and get its dimensions
track = pygame.image.load("assets/track.png")
track = pygame.transform.scale(
    track, (track.get_width() // 1.8, track.get_height() // 1.8))
WIDTH, HEIGHT = track.get_width(), track.get_height()

# Set up the display with dimensions matching the track image
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formulae!")

# Load the F1 car image and set its initial position
f1_car = pygame.image.load("assets/f1-car.png")
f1_car = pygame.transform.scale(f1_car, (50, 30))  # Resize for better gameplay
car_width, car_height = f1_car.get_width(), f1_car.get_height()
car_x, car_y = WIDTH // 3.8, HEIGHT // 3.8
car_speed = 0.5
max_speed = 2
acceleration = 0.1
friction = 0.05
turn_speed = 2
car_angle = 0

# Function to rotate the car image


def rotate_car(image, angle):
    return pygame.transform.rotate(image, angle)

# Function to calculate car corners after rotation


def get_car_corners(x, y, angle):
    cos_angle = math.cos(math.radians(angle))
    sin_angle = math.sin(math.radians(angle))

    # Half dimensions
    half_width = car_width / 2
    half_height = car_height / 2

    # Calculate corner positions
    corners = [
        (x + half_width * cos_angle - half_height * sin_angle + 0.8,
         y + half_width * sin_angle + half_height * cos_angle + 0.8),  # Top-right
        (x - half_width * cos_angle - half_height * sin_angle + 0.8,
         y - half_width * sin_angle + half_height * cos_angle + 0.8),  # Top-left
        (x - half_width * cos_angle + half_height * sin_angle + 0.8,
         y - half_width * sin_angle - half_height * cos_angle + 0.8),  # Bottom-left
        (x + half_width * cos_angle + half_height * sin_angle + 0.8,
         y + half_width * sin_angle - half_height * cos_angle + 0.8),  # Bottom-right
    ]
    return corners

# Function to check collision with white areas (off-track)


def is_off_track(corners):
    for corner in corners:
        x, y = corner
        # Ensure coordinates are within bounds
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            # Check for white
            if track.get_at((int(x), int(y)))[:3] == (255, 255, 255):
                return True
        else:
            return True  # Out of bounds is considered off-track
    return False


# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car_speed = min(car_speed + acceleration, max_speed)
    elif keys[pygame.K_DOWN]:
        car_speed = max(car_speed - acceleration * 2, -max_speed / 2)
    else:
        # Apply friction when no keys are pressed
        if car_speed > 0:
            car_speed = max(car_speed - friction, 0)
        elif car_speed < 0:
            car_speed = min(car_speed + friction, 0)

    if keys[pygame.K_LEFT]:
        # Slower turning at high speed
        car_angle += turn_speed * (1 - abs(car_speed) / max_speed)
    if keys[pygame.K_RIGHT]:
        car_angle -= turn_speed * (1 - abs(car_speed) / max_speed)

    # Calculate new position
    new_x = car_x + car_speed * pygame.math.Vector2(1, 0).rotate(-car_angle).x
    new_y = car_y + car_speed * pygame.math.Vector2(1, 0).rotate(-car_angle).y

    # Get new corners and check if off-track
    new_corners = get_car_corners(new_x, new_y, car_angle)
    if not is_off_track(new_corners):
        car_x, car_y = new_x, new_y  # Update position if on track
    else:
        car_speed = 0  # Stop the car if it goes off-track

    # Draw the track and car
    screen.blit(track, (0, 0))
    rotated_car = rotate_car(f1_car, car_angle)
    rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, rect.topleft)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
