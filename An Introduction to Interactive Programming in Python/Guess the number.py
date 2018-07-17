"""
Copy to codeskulptor.com and run.
"""

import random
import simplegui
import math

number = 0
game_range = 100
remaining_guesses = 0

def new_game():
	global number
	number = random.randint(0, game_range)
	print 'New game started'
	print 'Range is 0 to ' + str(game_range)
	print 'Enter your guess'
	global remaining_guesses
	remaining_guesses = math.ceil(math.log(game_range + 1, 2))
	print 'Number of remaining guesses is ' + str(int(remaining_guesses))

def range100():
	global game_range
	global remaining_guesses
	game_range = 100
	new_game()

def range1000():
	global game_range
	global remaining_guesses
	game_range = 1000
	new_game()

def input_guess(guess):
	global remaining_guesses
	guess = float(guess)
	if guess > number:
		print 'Lower!'
		remaining_guesses -= 1
		print 'Number of guesses left: ' + str(int(remaining_guesses))
		guesses_check()
	elif guess < number:
		print 'Higher!'
		remaining_guesses -= 1
		print 'Number of guesses left: ' + str(int(remaining_guesses))
		guesses_check()
	else:
		print 'Correct!'
		new_game()
		print 'New game started!'

def guesses_check():
	global remaining_guesses
	if remaining_guesses == 0:
		print 'Game over!'
		new_game()

frame = simplegui.create_frame('Guess the number', 200, 200)
button1 = frame.add_button('Set range to 1 to 100', range100)
button2 = frame.add_button('Set range to 1 to 1000', range1000)
inp = frame.add_input('Your guess', input_guess, 50)

new_game()