import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 500, 400
BALL_SPEED = 4
PADDLE_SPEED = 6
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_RADIUS = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Pong")

# Paddle and Ball Positions
player_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)

# Ball Velocity
ball_dx = BALL_SPEED * random.choice((1, -1))
ball_dy = BALL_SPEED * random.choice((1, -1))

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED
    
    # AI Paddle Movement (follows the ball)
    if ai_paddle.centery < ball.centery:
        ai_paddle.y += PADDLE_SPEED - 2  # AI speed is slightly reduced for fairness
    elif ai_paddle.centery > ball.centery:
        ai_paddle.y -= PADDLE_SPEED - 2
    
    # Ball Movement
    ball.x += ball_dx
    ball.y += ball_dy
    
    # Ball Collision with Walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1
    
    # Ball Collision with Paddles
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_dx *= -1
    
    # Scoring (reset ball if it goes off screen)
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_dx = BALL_SPEED * random.choice((1, -1))
        ball_dy = BALL_SPEED * random.choice((1, -1))
    
    # Draw Objects
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # Update Display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
