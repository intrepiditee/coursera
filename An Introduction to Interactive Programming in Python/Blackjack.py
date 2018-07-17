"""
Mini-project #6 - Blackjack

Copy to codeskulptor.com and run.
"""

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        cards = ''
        for card in self.cards:
            cards += str(card) + ' '
        return 'Hand contains ' + cards

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        is_A = False
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                is_A = True
        if is_A:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
        else:
            return value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + CARD_SIZE[0] * i, pos[1]])
            i += 1
        
# define deck class 
class Deck:
    def __init__(self):
        cards = []
        for suit in SUITS:
            for rank in RANKS:
                cards.append(Card(suit, rank))
        self.cards = cards

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()    

    def __str__(self):
        # return a string representing the deck
        deck = ' '
        for card in self.cards:
            deck += str(card) + ' '
        return deck


#define event handlers for buttons
def deal():
    global score, deck, outcome, in_play, Player, Dealer
    # your code goes here
    if in_play:
        score -= 1
    outcome = ''
    deck = Deck()
    deck.shuffle()
    Player = Hand()
    Dealer = Hand()
    for i in range(2):
        Player.add_card(deck.deal_card())
        Dealer.add_card(deck.deal_card())
    print str(Player), str(Dealer)
    outcome = 'Hit or stand?'
    print outcome
    in_play = True

def hit():
    global outcome, score, in_play
    # replace with your code below

    # if the hand is in play, hit the player
    if in_play:
        Player.add_card(deck.deal_card())
        print str(Player)
        if Player.get_value() > 21:
            outcome = 'You have busted. You lose.'
            print outcome
            score -= 1
            in_play = False
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, score, in_play
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if Player.get_value() > 21:
            outcome = 'You have busted. You lose.'
            score -= 1
        while Dealer.get_value() <= 17:
            Dealer.add_card(deck.deal_card())
            print str(Dealer)
        if Dealer.get_value() > 21:
            outcome = 'Dealer has busted. You win.'
            score += 1
        else:
            if Dealer.get_value() > Player.get_value():
                outcome = 'Your points are smaller. You lose.'
                score -= 1
            elif Dealer.get_value() == Player.get_value():
                outcome = 'Tie. You lose.'
                score -= 1
            else:
                outcome = 'Your points are larger. You win.'
                score += 1
        print outcome
        in_play = False
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    Dealer.draw(canvas, [100, 220])
    Player.draw(canvas, [100, 390])
    canvas.draw_text('Blackjack', [100, 100], 60, 'Black')
    canvas.draw_text(outcome, [100, 360], 30, 'Black')
    canvas.draw_text('Score = ' + str(score), [100, 160], 30, 'Black')
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_CENTER[0], 220 +CARD_CENTER[1]], CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
