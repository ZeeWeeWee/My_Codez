import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up the game window
width, height = 640, 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Danger Noodle")

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Snake properties
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"

# Food properties
food_pos = [random.randrange(1, (width//10)) * 10,
            random.randrange(1, (height//10)) * 10]
food_spawn = True

# Score
score = 0
high_score = 0

# Load high score from file
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Clock to control game speed
clock = pygame.time.Clock()

# Game over flag
game_over = False

def show_game_over_screen():
    global high_score

    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))

    font = pygame.font.SysFont(None, 60)
    game_over_text = font.render("Game Over", True, red)
    win.blit(game_over_text, (width//2 - game_over_text.get_width()//2, height//4 - game_over_text.get_height()//2))
    
    font = pygame.font.SysFont(None, 36)
    score_text = font.render("Score: " + str(score), True, green)
    high_score_text = font.render("High Score: " + str(high_score), True, green)
    restart_text = font.render("Press R to Restart", True, green)
    exit_text = font.render("Press Esc to Exit", True, green)
    win.blit(score_text, (width//2 - score_text.get_width()//2, height//2))
    win.blit(high_score_text, (width//2 - high_score_text.get_width()//2, height//2 + score_text.get_height()))
    win.blit(restart_text, (width//2 - restart_text.get_width()//2, height//2 + score_text.get_height() + high_score_text.get_height()))
    win.blit(exit_text, (width//2 - exit_text.get_width()//2, height//2 + score_text.get_height() + high_score_text.get_height() + restart_text.get_height()))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            snake_pos = [100, 50]
            snake_body = [[100, 50], [90, 50], [80, 50]]
            snake_direction = "RIGHT"
            food_pos = [random.randrange(1, (width//10)) * 10,
                        random.randrange(1, (height//10)) * 10]
            food_spawn = True
            score = 0
            game_over = False

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT] and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            if keys[pygame.K_RIGHT] and snake_direction != "LEFT":
                snake_direction = "RIGHT"
            if keys[pygame.K_UP] and snake_direction != "DOWN":
                snake_direction = "UP"
            if keys[pygame.K_DOWN] and snake_direction != "UP":
                snake_direction = "DOWN"

        # Move the snake...
        if snake_direction == "RIGHT":
            snake_pos[0] += 10
        if snake_direction == "LEFT":
            snake_pos[0] -= 10
        if snake_direction == "UP":
            snake_pos[1] -= 10
        if snake_direction == "DOWN":
            snake_pos[1] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (width//10)) * 10,
                        random.randrange(1, (height//10)) * 10]
        food_spawn = True

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
            game_over = True

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over = True

    win.fill(white)
    
    if game_over:
        show_game_over_screen()
    else:
        for pos in snake_body:
            pygame.draw.rect(win, green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(win, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    pygame.display.update()
    clock.tick(15)
