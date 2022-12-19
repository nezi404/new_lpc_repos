import turtle


# draw screen
screen = turtle.Screen()
screen.title("My Pong")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# draw paddle 1
paddle_1 = turtle.Turtle()
paddle_1.speed(0)
paddle_1.shape("square")
paddle_1.color("white")
paddle_1.shapesize(stretch_wid=5, stretch_len=1)
paddle_1.penup()
paddle_1.goto(-350, 0)

# draw paddle 2
paddle_2 = turtle.Turtle()
paddle_2.speed(0)
paddle_2.shape("square")
paddle_2.color("white")
paddle_2.shapesize(stretch_wid=5, stretch_len=1)
paddle_2.penup()
paddle_2.goto(350, 0)

# draw ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.5
ball.dy = 0.5

# score
score_1 = 0
score_2 = 0

# head-up display
hud = turtle.Turtle()
hud.speed(0)
hud.shape("square")
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 260)
hud.write("0 : 0", align="center", font=("Press Start 2P", 24, "normal"))


def paddle_1_up():
    y = paddle_1.ycor()
    if y < 250:
        y += 30
    else:
        y = 250
    paddle_1.sety(y)


def paddle_1_down():
    y = paddle_1.ycor()
    if y > -250:
        y += -30
    else:
        y = -250
    paddle_1.sety(y)


def paddle_2_up():
    y = paddle_2.ycor()
    if y < 250:
        y += 30
    else:
        y = 250
    paddle_2.sety(y)


def paddle_2_down():
    y = paddle_2.ycor()
    if y > -250:
        y += -30
    else:
        y = -250
    paddle_2.sety(y)


# keyboard
screen.listen()
screen.onkeypress(paddle_1_up, "w")
screen.onkeypress(paddle_1_down, "s")
screen.onkeypress(paddle_2_up, "Up")
screen.onkeypress(paddle_2_down, "Down")

while True:
    screen.update()
    # ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Collision with the upper wall and collision with lower wall
    def up_down_collision(cor_ball_y, ball_cor_y, set_value):
        if cor_ball_y > ball_cor_y:
            ball.sety(set_value)
            ball.dy *= -1

    # Collision with left wall and collision with right wall
    def left_right_collision(ball_cor_y, cor_ball_y, scoring_1, scoring_2):
        global score_1
        global score_2
        if ball_cor_y < cor_ball_y:
            ball.goto(0, 0)
            ball.dx *= -1
            score_1 += scoring_1
            score_2 += scoring_2
            hud.clear()
            hud.write("{} : {}".format(score_1, score_2), align="center", font=("Press Start 2P", 24, "normal"))
    
     # Paddle adjust: add one more condition for the x
    def paddle_checker(cor_ball_x, ball_cor_x, cor_ball_y, ball_cor_y, ball_kick):
        if cor_ball_x + 10 > ball_cor_x > (
                cor_ball_x - 10) and cor_ball_y + 50 > ball_cor_y > cor_ball_y - 50:
            ball.setx(ball.xcor() + ball_kick)
            ball.dx *= -1


    left_right_collision(ball.xcor(), -380, 0, 1)
    left_right_collision(390, ball.xcor(), 1, 0)
    up_down_collision(ball.ycor(), 290, 290)
    up_down_collision(-290, ball.ycor(), -290)
    paddle_checker(paddle_1.xcor(), ball.xcor(), paddle_1.ycor(), ball.ycor(), 10)
    paddle_checker(ball.xcor(), paddle_2.xcor(), ball.ycor(), paddle_2.ycor(), -10)
