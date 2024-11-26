import pygame
import sys

# Initialize Pygame
pygame.init()

# Load the track image and get its dimensions
track = pygame.image.load("assets/track.png")
track = pygame.transform.scale(
    track, (track.get_width() // 2.5, track.get_height() // 2.5))
WIDTH, HEIGHT = track.get_width(), track.get_height()

# Set up the display with dimensions matching the track image
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drive an F1 Car")

# Load the F1 car image and set its initial position
f1_car = pygame.image.load("assets/f1-car.png")
f1_car = pygame.transform.scale(f1_car, (50, 30))  # Resize for better gameplay
car_x, car_y = WIDTH // 2, HEIGHT // 2
car_speed = 5
car_angle = 0

# Function to rotate the car image


def rotate_car(image, angle):
    return pygame.transform.rotate(image, angle)


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
        car_x += car_speed * pygame.math.Vector2(1, 0).rotate(-car_angle).x
        car_y += car_speed * pygame.math.Vector2(1, 0).rotate(-car_angle).y
    if keys[pygame.K_DOWN]:
        car_x -= car_speed * pygame.math.Vector2(1, 0).rotate(-car_angle).x
        car_y -= car_speed * pygame.math.Vector2(1, 0).rotate(-car_angle).y
    if keys[pygame.K_LEFT]:
        car_angle += 5
    if keys[pygame.K_RIGHT]:
        car_angle -= 5

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
