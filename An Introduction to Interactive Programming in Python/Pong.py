"""
Implementation of classic arcade game Pong

Copy to codeskulptor.com and run.
"""

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
score1 = 0
score2 = 0
paddle1_pos = [0, HEIGHT / 2 + HALF_PAD_HEIGHT]
paddle2_pos = [WIDTH - PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT ]
paddle1_vel = 0
paddle2_vel = 0

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)
        ball_vel[1] = - random.randrange(60, 180)
    elif direction == LEFT:
        ball_vel[0] = - random.randrange(120, 240)
        ball_vel[1] = - random.randrange(60, 180)


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    if score2 >= score1:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, BALL_RADIUS
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0] / 60
    ball_pos[1] += ball_vel[1] / 60
            
    # draw ball
    canvas.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 1, 'Yellow', 'Yellow')
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] + paddle1_vel >= PAD_HEIGHT and paddle1_pos[1] + paddle1_vel <= HEIGHT:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] + paddle2_vel >= PAD_HEIGHT and paddle2_pos[1] + paddle2_vel <= HEIGHT:
        paddle2_pos[1] += paddle2_vel

    # draw paddles
    canvas.draw_polygon([paddle1_pos, [PAD_WIDTH, paddle1_pos[1]], [PAD_WIDTH, paddle1_pos[1] - PAD_HEIGHT], [0, paddle1_pos[1] - PAD_HEIGHT]], 1, 'Yellow', 'Yellow')
    canvas.draw_polygon([paddle2_pos, [WIDTH, paddle2_pos[1]], [WIDTH, paddle2_pos[1] - PAD_HEIGHT], [paddle2_pos[0], paddle2_pos[1] - PAD_HEIGHT]], 1, 'Yellow', 'Yellow')
    
    # determine whether paddle and ball collide    
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and paddle1_pos[1] - PAD_HEIGHT <= ball_pos[1] and ball_pos[1] <= paddle1_pos[1] and ball_vel[0] < 0:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = 1.1 * ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]
    elif ball_pos[0] >= WIDTH - BALL_RADIUS and paddle2_pos[1] - PAD_HEIGHT <= ball_pos[1] and ball_pos[1] <= paddle2_pos[1] and ball_vel[0] > 0:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] = 1.1 * ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]
    elif ball_pos[1] <= BALL_RADIUS and ball_vel[1] < 0:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS and ball_vel[1] > 0:
        ball_vel[1] = - ball_vel[1]

    # draw scores
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and ball_vel[0] < 0:
        if paddle1_pos[1] - PAD_HEIGHT > ball_pos[1] or paddle1_pos[1] < ball_pos[1]:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH and ball_vel[0] > 0:
        if paddle2_pos[1] - PAD_HEIGHT > ball_pos[1] or paddle2_pos[1] <  ball_pos[1]:
            score1 += 1
            spawn_ball(LEFT)

    canvas.draw_text(str(score1), [230, 40], 40, 'Yellow')
    canvas.draw_text(str(score2), [350, 40], 40, 'Yellow')

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 5 
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0 

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Reset', new_game)


# start frame
new_game()
frame.start()


