import pygame
import random

pygame.init()

WIDTH, HEIGHT = 449, 481
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My Car Game')

background_image = pygame.image.load('road.png').convert()
car_image = pygame.image.load('car.png').convert_alpha()
car_rect = car_image.get_rect()
car_rect.center = (WIDTH // 2, HEIGHT - 50)

obstacle_images = [
    pygame.image.load('obstacle1.png').convert_alpha(),
    pygame.image.load('obstacle2.png').convert_alpha(),
    pygame.image.load('obstacle3.png').convert_alpha()
]
obstacle_image = random.choice(obstacle_images)
obstacle_rect = obstacle_image.get_rect()
obstacle_rect.center = (random.randint(50, WIDTH - 50), -obstacle_rect.height)

score_font = pygame.font.Font(None, 36)
score = 0

game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WIDTH // 2, HEIGHT // 3)

paused_font = pygame.font.Font(None, 36)
paused_text = paused_font.render('Paused', True, (255, 255, 255))
paused_rect = paused_text.get_rect()
paused_rect.center = (WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()

game_over = False
paused = False
speed = 5

MENU_BG_COLOR = (128, 128, 128)
menu_bg = pygame.Surface((WIDTH, HEIGHT))
menu_bg.fill(MENU_BG_COLOR)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_SPACE:
                if game_over:
                    game_over = False
                    score = 0
                    car_rect.center = (WIDTH // 2, HEIGHT - 50)
                    obstacle_rect.center = (random.randint(50, WIDTH - 50), -obstacle_rect.height)
                    speed = 5

    if not game_over and not paused:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            car_rect.move_ip(-speed, 0)
        if keys[pygame.K_RIGHT]:
            car_rect.move_ip(speed, 0)

        # restrict car movement to game window
        car_rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        screen.blit(background_image, (0, 0))
        screen.blit(car_image, car_rect)

        obstacle_rect.move_ip(0, speed)
        if obstacle_rect.top > HEIGHT:
            obstacle_image = random.choice(obstacle_images)
            obstacle_rect = obstacle_image.get_rect()
            obstacle_rect.center = (random.randint(50, WIDTH - 50), -obstacle_rect.height)
            score += 1
            if score % 10 == 0:
                speed += 1

        screen.blit(obstacle_image, obstacle_rect)

        if car_rect.colliderect(obstacle_rect):
            game_over = True
            score += 1

        score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
    elif paused:
        screen.blit(paused_text, paused_rect)
    elif game_over:
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2))

    pygame.display.update()
    clock.tick(60)