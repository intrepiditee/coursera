"""
implementation of card game - Memory

Copy to codeskulptor.com and run.
"""

import simplegui
import random

number_list = [n for n in range(9)] * 2
state_list = [False] * 16
exposed_list = [False] * 16
state = 0
turn = 0
prev_number = 0
prev_prev_number = 0

# helper function to initialize globals
def new_game():
	global number_list, state_list, exposed_list, turn
    random.shuffle(number_list)
    state_list = [False] * 16
    exposed_list = [False] * 16
    turn = 0
    label.set_text('Turns = ' + str(turn))

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, state_list, exposed_list, turn, prev_number, prev_prev_number
    i = pos[0] // 50
    if state == 0 and state_list[i] == False and exposed_list[i] == False:
    	state_list[i] = True
    	prev_prev_number = i
    	turn += 1
    	state += 1
    elif state == 1 and state_list[i] == False and exposed_list[i] == False:
    	state_list[i] = True
    	prev_number = i
    	if number_list[prev_prev_number] == number_list[prev_number]:
    		exposed_list[prev_prev_number] = True
    		exposed_list[prev_number] = True
    	state += 1
    elif state == 2 and state_list[i] == False and exposed_list[i] == False:
    	state_list = [False] * 16
    	state_list[i] = True
    	prev_prev_number = i
    	turn += 1
    	state = 1
    label.set_text('Turns = ' + str(turn))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
	for i in range(16):
		if state_list[i] == False and exposed_list[i] == False:
			canvas.draw_polygon([[i * 50, 0], [i * 50, 100], [(i + 1) * 50, 100], [(i + 1) * 50, 0]], 5, 'Black', 'Green')
		else:
			canvas.draw_text(str(number_list[i]), [i * 50 + 17, 60], 30, 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button('Reset', new_game)
label = frame.add_label('Turns = 0')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric