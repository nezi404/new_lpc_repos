"""
The game experience is bad, but I tried to make it look like the original.
The Turtle is slow, I couldn't find the bug that let it that way.
"""
# Libraries needed
import time
import turtle


# The game screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(height=750, width=550)
screen.tracer(0)
# Game display
hud = turtle.Turtle()
hud.speed(0)
hud.shape("square")
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 320)
hud.write("0\t3 ", align="center", font=("Press Start 2P", 27, "normal"))

# Creating the paddle:
player = turtle.Turtle()
player.shape("square")
player.shapesize(stretch_wid=0.5, stretch_len=1.3)
player.color("blue")
player.penup()
player.goto(0, -340)
player.dx = 0.5

# Score and life_point
life_points = 3
# Paddle moves


def paddle_right():
    x = player.xcor()
    if x < 256:
        x += 30
    else:
        x = 256
    player.setx(x)


def paddle_left():
    x = player.xcor()
    if x > -256:
        x += -30
    else:
        x = -256
    player.setx(x)


# Keyboard section
screen.listen()
screen.onkeypress(paddle_right, "Right")
screen.onkeypress(paddle_left, "Left")

global brick

already_point = []
move = True
highest_score = 0
coordinate_x = -258
coordinate_y = 300


# Ball
ball = turtle.Turtle()
ball.shape("square")
ball.shapesize(stretch_wid=0.2, stretch_len=0.4)
ball.color("white")
ball.penup()
ball.goto(0, -330)
ball.dy = -3
ball.dx = -3
ball.speed(0)

while True:
    screen.update()
    # Ball settings
    ball.setx(ball.xcor() - ball.dx)
    ball.sety(ball.ycor() - ball.dy)


    def paddle_collision():
        global move
        if player.ycor() + 15 > ball.ycor() > player.ycor() - 15 \
                and player.xcor() + 26 > ball.xcor() > player.xcor() - 26\
                and move is False:
            ball.dy *= -1
            ball.dx *= -1
            ball.sety(ball.ycor()+10)
        if life_points <= 3:
            ball.sety(ball.ycor() + 10)
            ball.showturtle()
            move = False

    def walls_collision(ball_cor, wall, dx_value, dy_value, ball_x_y, ball_y_x):
        global move
        if ball_cor > wall:
            ball.dx *= dx_value
            ball.dy *= dy_value
            ball.goto(ball_x_y, ball_y_x)
            move = False


    def life_checker():
        global move, ball, life_points

        if ball.ycor() < -375:
            life_points -= 1
            hud.clear()
            hud.write(f"{highest_score}\t{life_points}", align="center", font=("Press Start 2P", 27, "normal"))
            player.goto(0, -340)
            ball.goto(0, -340)
            ball.dy = 3
            ball.dx = 3

    colour = 0
    # Creating the bricks
    for b in range(8):
            for a in range(18):
                if (coordinate_x, coordinate_y) not in already_point:  # Checking the brick hasn't been hit
                    # Choosing the appropriate colour for each row of bricks
                    colour = "white"
                    if b < 2:
                        colour = "red"
                    elif b < 4:
                        colour = "orange"
                    elif b < 6:
                        colour = "green"
                    elif b <= 8:
                        colour = "yellow"
                    # Creating the bricks
                    brick = turtle.Turtle()
                    brick.shape("square")
                    brick.shapesize(stretch_wid=0.5, stretch_len=1.3)
                    brick.color(str(colour))
                    brick.penup()
                    brick.goto(coordinate_x, coordinate_y)
                    brick.pendown()
                # Adding the scores for the hit bricks, and making them black
                if brick.ycor() + 15 > ball.ycor() > brick.ycor() - 15 \
                        and brick.xcor() + 10 > ball.xcor() > brick.xcor()\
                        - 10 and brick.pos() not in already_point:
                    if colour == "yellow":
                        highest_score += 1
                    if colour == "green":
                        highest_score += 3
                    if colour == "orange":
                        highest_score += 5
                    if colour == "red":
                        highest_score += 7
                    hud.clear()
                    hud.write(f"{highest_score}\t{life_points}", align="center", font=("Press Start 2P", 27, "normal"))
                    ball.goto(ball.xcor() - 10,  ball.ycor() - 20)  # Making the ball bounce
                    ball.dx = 10
                    ball.dy = 10
                    ball.dx *= 1
                    ball.dy *= 2
                    brick.color("black")  # I didn't understand why I couldn't use hideturtle(), so I made them black
                    point = 1
                    already_point.append(brick.pos())
                coordinate_x += 30
            coordinate_y = coordinate_y - 15
            coordinate_x = - 258
    coordinate_x = -258
    coordinate_y = 300

    # Calling my functions
    life_checker()
    paddle_collision()
    walls_collision(ball.xcor(), 260, -1, 1, ball.xcor() - 10, ball.ycor() + 10)
    walls_collision(-260, ball.xcor(), -1, 1, ball.xcor()+10, ball.ycor() - 10)
    walls_collision(ball.ycor(), 300, -1, -1, ball.xcor()-10, ball.ycor() - 10)

    # Game over screen
    if life_points == 0:
        hud.clear()
        over = turtle.Turtle()
        over.color("white")
        over.goto(0, 0)
        over.write("GAME OVER", align="center", font=("Press Start 2P", 50, "normal"))
        time.sleep(5)
        break
