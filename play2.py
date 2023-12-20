import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodging Game")

# Load and scale player image
player_size = (50, 50)
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
objects = []
object_speed = 5
score = 0

# Function to spawn objects on either the left or right side
def spawn_object():
    side = random.choice(['left', 'right'])
    if side == 'left':
        return pygame.Rect(0, random.randint(0, HEIGHT - 50), 20, 50)
    else:
        return pygame.Rect(WIDTH - 20, random.randint(0, HEIGHT - 50), 20, 50)

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

    # Spawn random objects
    if random.randint(1, 100) < 5:
        object_rect = spawn_object()
        objects.append(object_rect)

    # Move and draw objects
    for obj in objects:
        if obj.left < WIDTH and obj.right > 0:
            obj.x -= object_speed
        else:
            objects.remove(obj)

    # Check for collisions with player
    for obj in objects:
        if player_rect.colliderect(obj):
            running = False

    # Draw everything
    screen.fill(WHITE)
    screen.blit(player_image, player_rect)

    for obj in objects:
        pygame.draw.rect(screen, (255, 0, 0), obj)

    # Display the score
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
