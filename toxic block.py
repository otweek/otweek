import pygame
import sys
import random

# Başlatma
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toxic Block") # Oyun başlığı güncellendi
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Oyun Değişkenleri
score = 0
high_score = 0
game_over = False
player_y = 400
velocity_y = 0
gravity = 0.8
is_jumping = False

# Hız değişkenleri
base_speed = 7
current_speed = 7
obstacle_x = 900
obstacle_type = "single"

def reset_game():
    global player_y, obstacle_x, current_speed, score, game_over, obstacle_type
    player_y = 400
    obstacle_x = 900
    current_speed = base_speed
    score = 0
    game_over = False
    obstacle_type = "single"

while True:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if 300 <= event.pos[0] <= 500 and 250 <= event.pos[1] <= 300:
                reset_game()

    if not game_over:
        # Zıplama
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping:
            velocity_y = -16
            is_jumping = True
        
        velocity_y += gravity
        player_y += velocity_y
        if player_y >= 400:
            player_y = 400
            is_jumping = False
            
        # Engel Hareketi
        obstacle_x -= current_speed
        
        if obstacle_x < -100:
            obstacle_x = random.randint(800, 1200)
            obstacle_type = random.choice(["single", "double"])
            score += 1
            
            # Hızlanma mantığı
            current_speed = base_speed + (score * 0.2)
            
        # Çarpışma Kontrolü
        player_rect = pygame.Rect(100, player_y, 50, 50)
        obs1_rect = pygame.Rect(obstacle_x, 400, 50, 50)
        obs2_rect = pygame.Rect(obstacle_x + 60, 400, 50, 50)
            
        if player_rect.colliderect(obs1_rect) or (obstacle_type == "double" and player_rect.colliderect(obs2_rect)):
            game_over = True
            if score > high_score: high_score = score
            
        # Çizimler
        pygame.draw.rect(screen, (255, 0, 0), player_rect)
        pygame.draw.rect(screen, (0, 0, 255), obs1_rect)
        if obstacle_type == "double":
            pygame.draw.rect(screen, (0, 0, 255), obs2_rect)
            
    else:
        # Game Over Ekranı
        pygame.draw.rect(screen, (0, 255, 0), (300, 250, 200, 50))
        screen.blit(font.render("YENİDEN BAŞLA", True, (0, 0, 0)), (305, 260))

    # Skor ve Hız Bilgisi
    screen.blit(font.render(f"Skor: {score}  Rekor: {high_score}  Hız: {current_speed:.1f}", True, (0, 0, 0)), (10, 10))
    
    pygame.display.flip()
    clock.tick(60)