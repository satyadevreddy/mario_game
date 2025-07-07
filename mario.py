import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Load images
def load_img(name, scale=None):
    img = pygame.image.load(f"assets/ImagesSprites/{name}.png")
    return pygame.transform.scale(img, scale) if scale else img

mario_img = load_img("maryo", (40, 50))
dragon_img = load_img("dragon", (80, 80))
fireball_img = load_img("fireball", (30, 30))
platform_img = load_img("cactus_bricks", (150, 30))
fire_platform_img = load_img("fire_bricks", (150, 30))
start_screen = load_img("start", (WIDTH, HEIGHT))
end_screen = load_img("end", (WIDTH, HEIGHT))

# Player
player = pygame.Rect(100, 380, 40, 50)
velocity_y = 0
jumping = False
score = 0

# Platforms
platforms = [pygame.Rect(100, 430, 200, 30), pygame.Rect(350, 350, 150, 30)]
fire_platforms = [pygame.Rect(600, 300, 150, 30)]

# Dragon
dragon = pygame.Rect(700, 380, 80, 80)

# Fireball
fireball = pygame.Rect(dragon.x - 20, dragon.y + 20, 30, 30)
fireball_speed = -6

# Game State
game_running = False
game_over = False

# Show start screen
def show_screen(image):
    screen.blit(image, (0, 0))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Start screen
show_screen(start_screen)

# Game loop
while True:
    screen.fill((135, 206, 235))  # sky blue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_SPACE] and not jumping:
            velocity_y = -15
            jumping = True

    # Gravity
    velocity_y += 1
    player.y += velocity_y

    # Collision with platforms
    on_platform = False
    for plat in platforms:
        if player.colliderect(plat) and velocity_y > 0:
            player.y = plat.top - player.height
            velocity_y = 0
            jumping = False
            on_platform = True
            break

    if not on_platform and player.bottom >= HEIGHT:
        player.y = HEIGHT - player.height
        velocity_y = 0
        jumping = False

    # Draw platforms
    for plat in platforms:
        screen.blit(platform_img, plat.topleft)
    for plat in fire_platforms:
        screen.blit(fire_platform_img, plat.topleft)

    # Fire platform kills player
    for fire in fire_platforms:
        if player.colliderect(fire):
            game_over = True

    # Draw player
    screen.blit(mario_img, (player.x, player.y))

    # Draw dragon
    screen.blit(dragon_img, dragon.topleft)

    # Fireball movement
    fireball.x += fireball_speed
    if fireball.right < 0:
        fireball.x = dragon.x - 20

    screen.blit(fireball_img, fireball.topleft)

    # Collision with fireball
    if player.colliderect(fireball):
        game_over = True

    # Score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

    # Game over screen
    if game_over:
        pygame.time.delay(1000)
        show_screen(end_screen)
        pygame.quit()
        sys.exit()