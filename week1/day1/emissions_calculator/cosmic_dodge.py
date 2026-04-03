import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Dodge")

clock = pygame.time.Clock()

def draw_gradient(surface, color_top, color_bottom):
    """
    Draw a vertical gradient over the entire surface.
    """
    height = surface.get_height()
    for y in range(height):
        # Calculate the color at this line by linear interpolation.
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

class Star:
    """
    A simple star that drifts downwards.
    """
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)
    
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.size)

class Player:
    """
    The spaceship controlled by the player.
    """
    def __init__(self):
        self.width = 40
        self.height = 60
        # Start at the horizontal center, near the bottom.
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = 5
        self.color = (0, 255, 255)
    
    def move(self, dx):
        self.x += dx * self.speed
        # Keep the player inside the window.
        self.x = max(0, min(self.x, WIDTH - self.width))
    
    def draw(self, surface):
        # Draw the spaceship as a triangle.
        point1 = (self.x + self.width // 2, self.y)
        point2 = (self.x, self.y + self.height)
        point3 = (self.x + self.width, self.y + self.height)
        pygame.draw.polygon(surface, self.color, [point1, point2, point3])
    
    def get_rect(self):
        # Return a rectangle for collision detection (an approximation).
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    """
    Falling obstacle (a meteor) that the player must avoid.
    """
    def __init__(self):
        self.radius = random.randint(15, 30)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = -self.radius  # Start just above the top.
        self.speed = random.uniform(2, 5)
        # Randomize the color a bit for visual variety.
        self.color = (255, random.randint(100, 255), 0)
    
    def update(self):
        self.y += self.speed
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
    
    def off_screen(self):
        # Check if the obstacle has moved past the bottom.
        return self.y - self.radius > HEIGHT
    
    def collides_with(self, rect):
        """
        Check collision between a circle (this obstacle) and a rectangle (the player).
        """
        # Find the closest point on the rectangle to the circle.
        circle_distance_x = abs(self.x - (rect.x + rect.width / 2))
        circle_distance_y = abs(self.y - (rect.y + rect.height / 2))
        
        if circle_distance_x > (rect.width / 2 + self.radius):
            return False
        if circle_distance_y > (rect.height / 2 + self.radius):
            return False
        
        if circle_distance_x <= (rect.width / 2):
            return True
        if circle_distance_y <= (rect.height / 2):
            return True
        
        corner_distance_sq = (circle_distance_x - rect.width / 2) ** 2 + (circle_distance_y - rect.height / 2) ** 2
        return corner_distance_sq <= (self.radius ** 2)

def main():
    # Create a field of stars.
    stars = [Star() for _ in range(100)]
    
    player = Player()
    obstacles = []
    spawn_timer = 0
    spawn_interval = 1000  # Time (in milliseconds) between spawning obstacles.
    score = 0
    font = pygame.font.SysFont("Arial", 24)
    running = True

    while running:
        dt = clock.tick(60)  # Maintain 60 FPS and get the time since the last tick.
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle player input.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move(1)
        
        # Update star positions.
        for star in stars:
            star.update()
        
        # Spawn obstacles at intervals.
        spawn_timer += dt
        if spawn_timer > spawn_interval:
            spawn_timer = 0
            obstacles.append(Obstacle())
            # Gradually increase difficulty by shortening the spawn interval.
            if spawn_interval > 300:
                spawn_interval -= 5
        
        # Update obstacles.
        for obstacle in obstacles:
            obstacle.update()
        # Remove obstacles that have gone off the screen.
        obstacles = [ob for ob in obstacles if not ob.off_screen()]
        # Increment the score based on survival time.
        score += dt / 1000

        # Check for collisions between the player and any obstacle.
        player_rect = player.get_rect()
        for obstacle in obstacles:
            if obstacle.collides_with(player_rect):
                running = False

        # Draw the background with a gradient.
        background = pygame.Surface((WIDTH, HEIGHT))
        draw_gradient(background, (10, 10, 40), (0, 0, 0))
        screen.blit(background, (0, 0))
        
        # Draw stars.
        for star in stars:
            star.draw(screen)
        
        # Draw obstacles.
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw the player's spaceship.
        player.draw(screen)
        
        # Render and display the score.
        score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
    
    # When the game loop ends (collision), show a game over screen.
    game_over(font, score)

def game_over(font, score):
    """
    Display the game over screen and wait for any key press to exit.
    """
    game_over_text = font.render("Game Over!", True, (255, 50, 50))
    score_text = font.render(f"Final Score: {int(score)}", True, (255, 255, 255))
    continue_text = font.render("Press any key to exit", True, (200, 200, 200))
    
    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting = False
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
