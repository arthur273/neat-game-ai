import pygame
import random
import math
import sys
import os
import neat

size = (50,50)
WIDTH, HEIGHT = 800, 300
start_pos  = (WIDTH // 2, HEIGHT // 2)
WHITE = (255, 255, 255)
object_speed = 5
image_path = "car.png"
current_generation = 0 # Generation counter
class Dodger:
    def __init__(self):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos

        self.radars = [] # List For Sensors / Radars
        self.drawing_radars = [] # Radars To Be Drawn

        self.alive = True # Boolean To Check If Car is Crashed

        self.time = 0 # Time Passed

    def move(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += 5
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

    def check_collision(self, objects):
        for obj in objects:
            if self.rect.colliderect(obj):
                self.alive = False
                break
            elif (self.rect.top > HEIGHT) or (self.rect.bottom < 2) or (self.rect.left < 0) or (self.rect.right > WIDTH):
                self.alive = False
                break
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_radar(screen) #OPTIONAL FOR SENSORS
        self.draw_area(screen)

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.rect.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_radar(self, degree, game_objects):
        length = 0
        collided = False
        x = int(self.rect.center[0] + math.cos(math.radians(360 - (degree))) * length)
        y = int(self.rect.center[1] + math.sin(math.radians(360 - (degree))) * length)

        while length < 300:
            length = length + 1
            # Check for collisions with objects
            x = int(self.rect.center[0] + math.cos(math.radians(360 - (degree))) * length)
            y = int(self.rect.center[1] + math.sin(math.radians(360 - (degree))) * length)
            if collided:
                break
            if (y > HEIGHT) or (y < 0) or (x < 0) or (x > WIDTH):
                collided = True
            for obj in game_objects:
                if obj.colliderect(pygame.Rect(x, y, 1, 1)):  # Assuming 1x1 point collision
                    collided = True  # Set the collision flag
                    break  # Break out of the inner loop


        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.rect.center[0], 2) + math.pow(y - self.rect.center[1], 2)))
        self.radars.append([(x, y), dist])


    def check_area(self, game_objects, location, size):
            hit = False
            x = int(self.rect.center[0] + location[0] * size[0])
            y = int(self.rect.center[1] + location[1] * size[1])        
            if (y > HEIGHT) or (y < 0) or (x < 0) or (x > WIDTH):
                hit = True
            for obj in game_objects:
                if obj.colliderect(pygame.Rect(x, y, 1, 1)):  # Assuming 1x1 point collision
                    hit = True  # Set the collision flag
                    break  # Break out of the inner loop
        self.areas.append([(x, y), hit])            
    
    def draw_area(self, screen):
        # Optionally Draw All Sensors / areas
        for radar in self.area:
            position = radar[0]
            if(radar[1]) = True # if hit red 
                pygame.draw.circle(screen, (255, 0, 0), position, 5)
            if(radar[1]) = False # if not hit green 
                pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def update(self, game_objects):
        # Check Collisions And Clear Radars
        self.check_collision(game_objects)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(0, 360, 45):
            self.check_radar(d, game_objects)

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        # Basic Alive Function
        return self.alive

    def get_reward(self):
        # Calculate Reward (Maybe Change?)
        # return self.distance / 50.0
        return self.time

def run_simulation(genomes, config):
    
    # Empty Collections For Nets and Cars
    nets = []
    cars = []
    l_objects = []
    r_objects = []
    # Initialize PyGame And The Display
    pygame.init()
    #screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) 
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Dodger())

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    #game_map = pygame.image.load('map1.png').convert() # Convert Speeds Up A Lot

    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:# and car.rect.right < WIDTH:
                car.rect.x += 5
            elif choice == 1:# and car.rect.left > 0:
                car.rect.x -= 5 
            elif choice == 2:# and car.rect.bottom < HEIGHT:
                car.rect.y += 5
            elif choice == 3:# and car.rect.top > 0:
                car.rect.y -= 5
        

        # Spawn random objects
        if random.randint(1, 100) < 5:
            object_height = random.randint(20, 50)
            object_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - object_height), 20, object_height)
            r_objects.append(object_rect)
        if random.randint(1, 100) < 5:
            object_height = random.randint(20, 50)
            object_rect = pygame.Rect(0, random.randint(0, HEIGHT - object_height), 20, object_height)
            #l_objects.append(object_rect)

        # Move and draw objects
        for obj in r_objects:
            obj.x -= object_speed
        # for obj in l_objects:
        #     obj.x += object_speed
        # Remove objects that are off the screen
        r_objects = [obj for obj in r_objects if obj.right > 0]
       # l_objects = [obj for obj in l_objects if obj.left < WIDTH]

        
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                car.time += 1
                still_alive += 1
                car.update(r_objects )#+ l_objects)
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40: # Stop After About 20 Seconds
            break

        # Draw everything
        screen.fill(WHITE)
        # screen.blit("car.png", player_rect)
        for car in cars:
            if car.is_alive():
                car.draw(screen)

        k = 0
        for obj in r_objects:
            pygame.draw.rect(screen, (255, 0, 0), r_objects[k])
            # if k < len(l_objects):
            #     pygame.draw.rect(screen, (255, 0, 0), l_objects[k])
            k += 1
        # Display the score
        # score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        # screen.blit(score_text, (10, 10))
        
        # Display Info
        text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60) # 60 FPS

if __name__ == "__main__":
    
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)

# object_speed = 5
# WHITE = (255, 255, 255)


# # Initialize Pygame
# pygame.init()

# # Set up display
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Dodging Game")

# # Colors
# WHITE = (255, 255, 255)

# # Clock and font for controlling the frame rate
# clock = pygame.time.Clock()
# font = pygame.font.Font(None, 36)

# # Game variables
# r_objects = []
# l_objects = []
# object_speed = 5
# score = 0

# # Create Dodger object
# player_size = (50, 50)
# player_start_pos = (WIDTH // 2, HEIGHT // 2)
# player = Dodger('car.png', player_size, player_start_pos)



# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Move the player with arrow keys
#     keys = pygame.key.get_pressed()
#     player.move(keys)

#     # Spawn random objects
#     if random.randint(1, 100) < 5:
#         object_height = random.randint(20, 50)
#         object_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - object_height), 20, object_height)
#         r_objects.append(object_rect)
#     if random.randint(1, 100) < 5:
#         object_height = random.randint(20, 50)
#         object_rect = pygame.Rect(0, random.randint(0, HEIGHT - object_height), 20, object_height)
#         l_objects.append(object_rect)

#     # Move and draw objects
#     for obj in r_objects:
#         obj.x -= object_speed
#     for obj in l_objects:
#         obj.x += object_speed

#     # Remove objects that are off the screen
#     r_objects = [obj for obj in r_objects if obj.right > 0]
#     l_objects = [obj for obj in l_objects if obj.left < WIDTH]

#     # Check for collisions with player
#     if player.check_collision(r_objects + l_objects):
#         running = False

#     # Draw everything
#     screen.fill(WHITE)
#     player.draw(screen)

#     for obj in r_objects + l_objects:
#         pygame.draw.rect(screen, (255, 0, 0), obj)
#     # Display the score
#     score_text = font.render(f'Score: {score}', True, (0, 0, 0))
#     screen.blit(score_text, (10, 10))

#     # Update the display
#     pygame.display.flip()

#     # Control the frame rate
#     clock.tick(30)

# # Quit Pygame
# pygame.quit()
