import pygame
import random
import time

# Initialize pygame
pygame.init()

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load background image
background = pygame.image.load("Grid.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 36)


def draw_text(text, color, x, y):
    text_obj = font.render(text, 1, color)
    screen.blit(text_obj, (x, y))


def display_winner(winner_text):
    screen.fill(WHITE)
    draw_text(winner_text, (0, 0, 0), WIDTH // 2 - 100, HEIGHT // 2)
    pygame.display.flip()
    time.sleep(3)


def reset_square():
    global timer_start, timer_duration, square_color
    timer_start = time.time()
    timer_duration = random.uniform(2, 7)
    square_color = RED


def main():
    global square_color
    running = True
    reset_square()

    p1_score = 0
    p2_score = 0

    p1_lockout = False
    p2_lockout = False

    while running:
        # Draw background image
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, square_color,
                         (WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100))

        draw_text(f"P1: {p1_score}", ORANGE, 10, 10)
        draw_text(f"P2: {p2_score}", BLUE, WIDTH - 110, 10)

        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if square_color == GREEN:
                    if event.key == pygame.K_a and not p1_lockout:
                        p1_score += 1
                        square_color = ORANGE
                        reset_square()
                    elif event.key == pygame.K_l and not p2_lockout:
                        p2_score += 1
                        square_color = BLUE
                        reset_square()
                else:
                    if event.key == pygame.K_a:
                        p1_lockout = True
                        p1_lockout_start = current_time
                    elif event.key == pygame.K_l:
                        p2_lockout = True
                        p2_lockout_start = current_time

        if p1_lockout and current_time - p1_lockout_start > 1:
            p1_lockout = False

        if p2_lockout and current_time - p2_lockout_start > 1:
            p2_lockout = False

        if current_time - timer_start > timer_duration and square_color != GREEN:
            square_color = GREEN

        if p1_score == 5 or p2_score == 5:
            break

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    if p1_score > p2_score:
        winner = "Player 1"
    else:
        winner = "Player 2"

    winner_text = f"{winner} wins!"
    display_winner(winner_text)

    pygame.quit()


if __name__ == "__main__":
    main()
