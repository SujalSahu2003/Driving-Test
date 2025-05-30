import pygame
from pygame.locals import *
import time
import random

# Set the size of the window
size = width, height = (500, 500)

# Define road properties
road_w = int(width / 1.4)
roadmark_w = int(width / 50)
green_area_start = width / 2 - road_w / 2
green_area_end = width / 2 + road_w / 2
yellow_line_y = 0
yellow_line_gap = 100
yellow_line_width = 60
yellow_line_speed = 5

# Car speed and acceleration
car_speed = 0
car_max_speed = 10
car_acceleration = 0.2
car_deceleration = 0.1

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((size))
pygame.display.set_caption('🌟 Road Racer - A Driving Test by Sujal Kumar Sahu 🌟')
icon = pygame.image.load('images/car_1.png')
pygame.display.set_icon(icon)

# Load images
car = pygame.transform.scale(pygame.image.load('images/car_1.png'), (50, 100))
car2 = pygame.transform.scale(pygame.image.load('images/car_2.png'), (50, 100))
car3 = pygame.transform.scale(pygame.image.load('images/car_3.png'), (50, 100))
crash_image = pygame.transform.scale(pygame.image.load('images/crash.png'), (100, 100))
vegetation_img = pygame.transform.scale(pygame.image.load('images/vegetation.png'), (40, 40))

# Rects
car_loc = car.get_rect(center=(width / 2 + road_w / 4, height * 0.8))
car2_loc = car2.get_rect(center=(width / 2 + road_w / 4, -height))
car3_loc = car3.get_rect(center=(width / 2 - road_w / 4, height))
crash_rect = crash_image.get_rect()

# Speeds
car2_speed = 5
car3_speed = 4
vegetation_speed = 3
vegetation_list = []
vegetation_frequency = 250
vegetation_counter = 0

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 30)
large_font = pygame.font.Font(None, 60)

# Colors
BACKGROUND_COLOR = (50, 150, 50)
ROAD_COLOR = (40, 40, 40)
LINE_COLOR = (255, 240, 60)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game states
game_over = False
start_menu = True
paused = False
score = 0
start_time = None
penalty_time = 5

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if start_menu and event.key == K_RETURN:
                start_menu = False
                score = 0
            elif paused and event.key == K_p:
                paused = False
            elif not start_menu and not paused and event.key == K_p:
                paused = True
            elif game_over and event.key == K_r:
                game_over = False
                car_loc.center = width / 2 + road_w / 4, height * 0.8
                car2_loc.center = width / 2 + road_w / 4, -height
                car3_loc.center = width / 2 - road_w / 4, height
                score = 0
                vegetation_list = []

    if start_menu:
        screen.fill(BACKGROUND_COLOR)
        title = large_font.render('-- Road Racer --', True, WHITE)
        prompt = small_font.render('Press ENTER to Start', True, WHITE)
        instructions1 = small_font.render('Use Left Arrow / Right Arrow or A / D to Move', True, WHITE)
        instructions2 = small_font.render('Press P to Pause the Game', True, WHITE)
        screen.blit(title, title.get_rect(center=(width // 2, height // 2 - 100)))
        screen.blit(prompt, prompt.get_rect(center=(width // 2, height // 2 - 40)))
        screen.blit(instructions1, instructions1.get_rect(center=(width // 2, height // 2 + 10)))
        screen.blit(instructions2, instructions2.get_rect(center=(width // 2, height // 2 + 40)))
    elif paused:
        pause_text = font.render('Paused - Press P to Resume', True, WHITE)
        screen.blit(pause_text, pause_text.get_rect(center=(width // 2, height // 2)))
    else:
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[K_LEFT] or keys[K_a]:
                if car_speed > -car_max_speed:
                    car_speed -= car_acceleration
            elif keys[K_RIGHT] or keys[K_d]:
                if car_speed < car_max_speed:
                    car_speed += car_acceleration
            else:
                car_speed = max(min(car_speed - car_deceleration, car_max_speed), -car_max_speed) if car_speed > 0 else min(max(car_speed + car_deceleration, -car_max_speed), car_max_speed)

            car_loc.centerx += car_speed
            if green_area_start <= car_loc.centerx <= green_area_end - car.get_width():
                if start_time is None:
                    start_time = time.time()
                elif time.time() - start_time > penalty_time:
                    score = max(0, score - 1)
                    start_time = None
            else:
                start_time = None

            if car_loc.centerx > green_area_end - car.get_width() / 2:
                car_loc.centerx = green_area_end - car.get_width() / 2
            elif car_loc.centerx < green_area_start + car.get_width() / 2:
                car_loc.centerx = green_area_start + car.get_width() / 2

            car2_loc.centery += car2_speed
            if car2_loc.top > height:
                car2_loc.center = width / 2 + road_w / 4, -height
                score += 1

            car3_loc.centery += car3_speed
            if car3_loc.top > height:
                car3_loc.center = width / 2 - road_w / 4, -height
                score += 1

            if car_loc.colliderect(car2_loc) or car_loc.colliderect(car3_loc):
                game_over = True
                crash_rect.center = car_loc.center

            yellow_line_y += yellow_line_speed
            if yellow_line_y > yellow_line_gap:
                yellow_line_y = 0

            for vegetation_rect in vegetation_list:
                vegetation_rect.y += vegetation_speed
                if vegetation_rect.y > height:
                    vegetation_rect.x = random.choice([
                        random.randint(0, int(green_area_start) - vegetation_rect.width),
                        random.randint(int(green_area_end), width - vegetation_rect.width)])
                    vegetation_rect.y = -vegetation_rect.height

            vegetation_counter += 0.5
            if vegetation_counter >= vegetation_frequency:
                vegetation_counter = 0
                vegetation_rect = vegetation_img.get_rect()
                vegetation_rect.x = random.choice([
                    random.randint(0, int(green_area_start) - vegetation_rect.width),
                    random.randint(int(green_area_end), width - vegetation_rect.width)])
                vegetation_rect.y = -vegetation_rect.height
                vegetation_list.append(vegetation_rect)

        # Drawing
        if game_over:
            screen.fill(BACKGROUND_COLOR)  # Green background on crash
            screen.blit(crash_image, crash_rect)
            over_text = font.render('GAME OVER', True, WHITE)
            score_display = font.render(f'Score: {score}', True, RED)
            restart_prompt = small_font.render('Press R to Restart', True, BLACK)
            screen.blit(over_text, over_text.get_rect(center=(width // 2, height // 2 - 60)))
            screen.blit(score_display, score_display.get_rect(center=(width // 2, height // 2)))
            screen.blit(restart_prompt, restart_prompt.get_rect(center=(width // 2, height // 2 + 60)))
        else:
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(screen, ROAD_COLOR, (width / 2 - road_w / 2, 0, road_w, height))
            pygame.draw.rect(screen, WHITE, (width / 2 - road_w / 2 + roadmark_w * 2 / 2, 0, roadmark_w, height))
            pygame.draw.rect(screen, WHITE, (width / 2 + road_w / 2 - roadmark_w * 4 / 2, 0, roadmark_w, height))

            current_line_y = yellow_line_y
            while current_line_y < height:
                yellow_line_rect = pygame.Rect(width / 2 - roadmark_w / 2, current_line_y, roadmark_w, yellow_line_width)
                pygame.draw.rect(screen, LINE_COLOR, yellow_line_rect)
                current_line_y += 2 * yellow_line_gap

            screen.blit(car, car_loc)
            screen.blit(car2, car2_loc)
            screen.blit(car3, car3_loc)

            for vegetation_rect in vegetation_list:
                screen.blit(vegetation_img, vegetation_rect)

        # Always display score (shifted slightly inward)
        score_text = small_font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (100, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()