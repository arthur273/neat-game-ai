import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodging Game")

# Load player image
player_size = (50, 50)  # Specify the size of the player
player_image = pygame.image.load('car.png')
player_image = pygame.transform.scale(player_image, player_size)
player_rect = player_image.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT // 2)

# Colors
WHITE = (255, 255, 255)

# Clock and font for controlling the frame rate
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Game variables
r_objects = []
l_objects = []
object_speed = 5
score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= 5
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += 5
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += 5

    # Spawn random objects
    if random.randint(1, 100) < 5:
        object_height = random.randint(20, 50)
        object_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - object_height), 20, object_height)
        r_objects.append(object_rect)
    if random.randint(1, 100) < 5:
        object_height = random.randint(20, 50)
        object_rect = pygame.Rect(0, random.randint(0, HEIGHT - object_height), 20, object_height)
        l_objects.append(object_rect)

    # Move and draw objects
    for obj in r_objects:
        obj.x -= object_speed
    for obj in l_objects:
        obj.x += object_speed
    # Remove objects that are off the screen
    r_objects = [obj for obj in r_objects if obj.right > 0]
    l_objects = [obj for obj in l_objects if obj.left < WIDTH]
    # Check for collisions with player
    j = 0
    for obj in r_objects:
        if player_rect.colliderect(r_objects[j]):
            running = False
        if j < len(l_objects):
            if player_rect.colliderect(l_objects[j]):
                running = False
        j += 1
    # Draw everything
    screen.fill(WHITE)
    screen.blit(player_image, player_rect)

    k = 0
    for obj in r_objects:
        pygame.draw.rect(screen, (255, 0, 0), r_objects[k])
        if k < len(l_objects):
            pygame.draw.rect(screen, (255, 0, 0), l_objects[k])
        k += 1
    # Display the score
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
