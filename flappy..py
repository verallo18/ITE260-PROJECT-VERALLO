import pygame
import sys
import random

pygame.init()

# Window setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

clock = pygame.time.Clock()

# Bird settings
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 15
bird_velocity = 0
gravity = 0.3
jump_strength = -8

# Pipe settings
pipe_width = 60
pipe_gap = 200
pipe_speed = 3
pipes = []

# Game state
score = 0
font = pygame.font.SysFont("Arial", 32)
game_over = False


def create_pipe():
    gap_y = random.randint(100, HEIGHT - 100)
    return {
        "x": WIDTH,
        "top_height": gap_y - pipe_gap // 2,
        "bottom_y": gap_y + pipe_gap // 2,
        "scored": False,  # prevents double counting
    }


def reset():
    global bird_y, bird_velocity, pipes, score, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False


def check_collision():
    # Bird hitting top/bottom
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
        return True

    # Bird hitting pipes
    for pipe in pipes:
        if bird_x + bird_radius > pipe["x"] and bird_x - bird_radius < pipe["x"] + pipe_width:
            if bird_y - bird_radius < pipe["top_height"] or bird_y + bird_radius > pipe["bottom_y"]:
                return True

    return False


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_strength

            if event.key == pygame.K_r:
                reset()

    # If game over, draw screen and skip physics
    if game_over:
        screen.fill((0, 0, 0))
        over_text = font.render("GAME OVER! Press R", True, (255, 50, 50))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(over_text, (40, HEIGHT // 2 - 20))
        screen.blit(score_text, (140, HEIGHT // 2 + 30))
        pygame.display.update()
        clock.tick(60)
        continue

    # Bird physics
    bird_velocity += gravity
    bird_y += bird_velocity

    # Pipe creation
    if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - 200:
        pipes.append(create_pipe())

    # Move pipes
    for pipe in pipes:
        pipe["x"] -= pipe_speed

        # Score when the bird passes the pipe center
        if not pipe["scored"] and pipe["x"] + pipe_width < bird_x:
            score += 1
            pipe["scored"] = True

    # Remove old pipes
    pipes = [p for p in pipes if p["x"] + pipe_width > 0]

    # Check collision
    if check_collision():
        game_over = True

    # Draw everything
    screen.fill((135, 206, 235))  # sky blue

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 200, 0), (pipe["x"], 0, pipe_width, pipe["top_height"]))
        pygame.draw.rect(screen, (0, 200, 0), (pipe["x"], pipe["bottom_y"], pipe_width, HEIGHT - pipe["bottom_y"]))

    # Draw bird
    pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), bird_radius)

    # Draw score
    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)
