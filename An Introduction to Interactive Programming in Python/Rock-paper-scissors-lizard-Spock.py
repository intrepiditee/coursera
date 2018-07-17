from random import randint

choices_table = {
    0: 'rock',
    1: 'paper',
    2: 'scissors',
    3: 'lizard',
    4: 'Spock'
}

def number2word(number):
    word = choices_table[number]
    return word

def word2number(word):
    for number, choice in choices_table.items():
        if word == choice:
            return number

def pc1_choice():
    pc1_numberchoice = randint(0, 4)
    pc1_choice = number2word(pc1_numberchoice)
    print "Computer 1 chose " + pc1_choice
    return pc1_choice


def pc2_choice():
    pc2_numberchoice = randint(0, 4)
    pc2_choice = number2word(pc2_numberchoice)
    print "Computer 2 chose " + pc2_choice
    return pc2_choice

def is_alive(my_choice, pc1_choice, pc2_choice):
    if word2number(pc1_choice) - word2number(my_choice) == 1 or word2number(pc1_choice) - word2number(my_choice) == -2:
        return False
    elif word2number(pc2_choice) - word2number(my_choice) == 1 or word2number(pc2_choice) - word2number(my_choice) == -2:
        return False
    else:
        return True

def who_wins():
    if is_alive(my_choice, pc1_choice, pc2_choice) == True and is_alive(pc1_choice, pc2_choice, my_choice) == False and is_alive(pc2_choice, pc1_choice, my_choice) == False:
        print 'You win!'
    elif is_alive(my_choice, pc1_choice, pc2_choice) == False and is_alive(pc1_choice, pc2_choice, my_choice) == True and is_alive(pc2_choice, pc1_choice, my_choice) == False:
        print 'Computer 2 wins.'
    elif is_alive(my_choice, pc1_choice, pc2_choice) == False and is_alive(pc1_choice, pc2_choice, my_choice) == False and is_alive(pc2_choice, pc1_choice, my_choice) == True:
        print 'Computer 3 wins.'
    else:
        print 'No one wins.'

my_choice = raw_input('rock, paper, scissors, lizard, or Spock?')
print 'You chose ' + my_choice
pc1_choice = pc1_choice()
pc2_choice = pc2_choice()
who_wins()