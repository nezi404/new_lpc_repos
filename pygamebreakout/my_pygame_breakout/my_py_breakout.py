import pygame
import random

pygame.init()
screen = pygame.display.set_mode([575, 750])

# Colours
colour_green = (0, 240, 200)
colour_red = (255, 0, 0)
colour_yellow = (255, 255, 0)
colour_orange = (255, 125, 0)
colour_black = (0, 0, 0)
colour_white = (255, 255, 255)

# Player
player = pygame.image.load("assets/player.png")
player_right = False
player_left = False
player_y = 700
player_x = 282

# Ball
ball = pygame.image.load("assets/ball.png")
ball_y = 700
ball_x = 282
ball_dx = -3
ball_dy = -3
ball_random_x = [1, -1]

# Life point related and game over screen
life_points = 1
geral_font = pygame.font.Font('assets/PressStart2P.ttf', 44)
life_text = geral_font.render('3', True, colour_white, colour_black)
life_text_rect = life_text.get_rect()
life_text_rect.center = (350, 50)
game_over_font = pygame.font.Font('assets/PressStart2P.ttf', 50)
game_over_text = game_over_font.render('GAME OVER', True, colour_white, colour_black)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (283, 350)

# Score display
score = 0
score_text = geral_font.render('0000', True, colour_white, colour_black)
score_text_rect = score_text.get_rect()
score_text_rect.center = (100, 50)
win_font = pygame.font.Font('assets/PressStart2P.ttf', 50)
win_text = win_font.render('YOU-WON', True, colour_white, colour_black)
win_rect = win_text.get_rect()
win_rect.center = (283, 350)


# player movement
def player_move(player_direction, move_value):
    global player_x
    if player_direction:
        player_x += move_value
        if player_x <= 0:
            player_x = 0
        if player_x >= 549:
            player_x = 549


# Player's paddle collision
def paddle_collision():
    global ball_dx, ball_dy, ball_x, ball_y
    if ball_x + 4 >= player_x >= ball_x - 29 and ball_y + 4 >= player_y >= ball_y - 16:
        ball_dy *= -1
        ball_dx *= -1
        ball_y -= 1
        print("AAAAAAAAAA")


# Wall collision and life checker
def wall_collision(ballwall, wallball, ball_dx_, ball_dy_):
    global ball_dy, ball_dx, life_points, ball_y, ball_x, life_text, player_x, player_y
    if ballwall >= wallball:
        ball_dx *= -ball_dx_
        ball_dy *= ball_dy_
        if ballwall == 70:
            ball_dy = (ball_dy / ball_dy) * 3
            ball_dx = (ball_dx / ball_dx) * 3
            ball_dx *= 2
        if ball_y >= 745:
            life_points += 1
            life_text = geral_font.render(f'{life_points}', True, colour_white, colour_black)
            ball_y = 700
            ball_x = 282
            player_y = 700
            player_x = 282
            ball_dy = (ball_dy/ball_dy)*3
            ball_dx = (ball_dx/ball_dx)*3
            ball_dx *= -ball_dx_
            ball_dy *= -ball_dy_


# Matrix that'll contain bricks coordinates
already_point = []
brick_x = 0.1
brick_y = 150


# Bricks creation and score checking
def bricks():
    global brick_y, brick_x, ball_dx, ball_dy, ball_x, ball_y, score, score_text
    colour = colour_red
    for column in range(8):
        for line in range(18):
            if column > 1:
                colour = colour_orange
            if column > 3:
                colour = colour_green
            if column > 5:
                colour = colour_yellow
            brick_pos = (brick_x, brick_y)
            if brick_pos not in already_point:
                brick = pygame.Rect(brick_x, brick_y, 30, 10)
                pygame.draw.rect(screen, colour, brick)
                # Check if the player scored
                if (ball_y + 6 >= brick_y > ball_y - 6 or
                    ball_y + 6 >= brick_y - 6 > ball_y - 6) \
                        and (ball_x - 10 <= brick_x + 6 < ball_x + 10
                             or ball_x - 10 <= brick_x - 6 < ball_x + 10):
                    brick_pos = (brick_x, brick_y)
                    already_point.append(brick_pos)
                    ball_y += 15
                    ball_dx *= randomly
                    ball_dy *= -1
                    score = int(score)
                    if column > 1:
                        score += 1
                    elif column > 3:
                        score += 3
                    elif column > 5:
                        score += 5
                    else:
                        score += 7
                    score = format(score, "04")
                    score_text = geral_font.render(f'{score}', True, colour_white, colour_black)

            brick_x += 32
        brick_y += 12
        brick_x = 0.1
    brick_x = 0.1
    brick_y = 150


pygame.display.flip()
game_clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Left and right keys moving events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_right = True
            if event.key == pygame.K_LEFT:
                player_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_right = False
            if event.key == pygame.K_LEFT:
                player_left = False

    if life_points < 4:
        screen.fill(colour_black)
        bricks()
        # Ball
        ball_x = ball_x + ball_dx
        ball_y = ball_y + ball_dy
        randomly = random.choice(ball_random_x)

        wall_collision(ball_y, 750, 1, -1)
        wall_collision(ball_x, 575, 1, 1)
        wall_collision(70, ball_y, randomly, -1)
        wall_collision(0, ball_x, 1, 1)

        #  keystroke events

        paddle_collision()
        player_move(player_right, 5)
        player_move(player_left, -5)

        # Drawing objects
        screen.blit(score_text, score_text_rect)
        screen.blit(life_text, life_text_rect)
        screen.blit(ball, (ball_x, ball_y))
        screen.blit(player, (player_x, 720))
    if life_points > 3:
        player = pygame.image.load("assets/player_game_over.png")
        player_y = 700
        player_x = 0.1
        ball_ = pygame.Rect(280, 680, 30, 30)
        pygame.draw.rect(screen, colour_black, ball_)
        screen.blit(player, (player_x, 720))
        screen.blit(game_over_text, game_over_rect)
    if score == 2:
        screen.blit(win_text, win_rect)

    pygame.display.flip()
    game_clock.tick(60)
