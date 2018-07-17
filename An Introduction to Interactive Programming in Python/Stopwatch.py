"""
Template for "Stopwatch: The Game"

Copy to codeskulptor.com and run.
"""

import simplegui

# define global variables

t = 0
success = 0
total = 0
is_started = False


# define helper function format that converts t
# in tenths of seconds into formatted string A:BC.D

def format(t):
    A = str(t // 600)
    if len(str(t % 600)) == 1:
        B = '0'
        C = '0'
        D = str(t % 600)[0]
        return A + ':' + B + C +'.' + D
    elif len(str(t % 600)) == 2:
        B = '0'
        C = str(t % 600)[0]
        D = str(t % 600)[1]
        return A + ':' + B + C +'.' + D
    elif len(str(t % 600)) == 3:
        B = str(t % 600)[0]
        C = str(t % 600)[1]
        D = str(t % 600)[2]
        return A + ':' + B + C +'.' + D

# define event handlers for buttons; "Start", "Stop", "Reset"


def button_start():
    global is_started
    timer.start()
    is_started = True


def button_stop():
    global total
    global is_started
    global success
    timer.stop()
    if is_started == True:
        total += 1
        if str(t)[-1] == "0":
            success += 1
    is_started = False

def button_reset():
    global t
    global is_started
    global success
    global total
    timer.stop()
    t = 0
    is_started = False
    success = 0
    total = 0

# define event handler for timer with 0.1 sec interval

def timer_handler():
    global t
    t += 1

# define draw handler

def draw(canvas):
    canvas.draw_text(format(t), [105, 175], 80, 'Red')
    canvas.draw_text(str(success) + "/" + str(total), [310, 55], 60, 'Red')
    
# create frame

frame = simplegui.create_frame('StopWatch', 400, 300)

# register event handlers

timer = simplegui.create_timer(100, timer_handler)
button1 = frame.add_button('Start', button_start)
button2 = frame.add_button('Stop', button_stop)
button3 = frame.add_button('Reset', button_reset)
frame.set_draw_handler(draw)


# start frame

frame.start()

# Please remember to review the grading rubric


