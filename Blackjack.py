# Mini-project #6 - Blackjack

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
message = ""
outcome = ""
score_dealer = 0
score_player = 0

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
        ans = "Hand contains "
        for i in range(len(self.cards)):
            if i == len(self.cards) - 1:
                ans = ans + str(self.cards[i]) + "."
            else:
                ans = ans + str(self.cards[i]) + ", "
        return ans

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        has_ace = False
        total = 0
        for card in self.cards:
            value = VALUES[card.get_rank()]
            total = total + value
            if card.get_rank() == 'A':
                has_ace = True
        if has_ace:
            if total + 10 <=21:
                return total + 10
            else:
                return total
        else:
            return total

    def draw(self, canvas, pos):
        pos_card = [0,0]
        for i in range(min(6,len(self.cards))):
            pos_card[0] = pos[0] + i * (CARD_SIZE[0] + 15)
            pos_card[1] = pos[1]
            self.cards[i].draw(canvas,pos_card)


# define deck class
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        ans = "Deck contains "
        for i in range(len(self.cards)):
            if i == len(self.cards) - 1:
                ans = ans + str(self.cards[i]) + "."
            else:
                ans = ans + str(self.cards[i]) + ", "
        return ans



#define event handlers for buttons
def deal():
    global outcome, message, in_play, deck, player, dealer, score_dealer
    if in_play:
        outcome =  "Dealer wins!"
        score_dealer += 1
    else:
        outcome = ""
    # your code goes here
    deck = Deck()
    player = Hand()
    dealer = Hand()
    deck.shuffle()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    #print "palyer:::" + str(player)
    #print "dealer:::" + str(dealer)
    message = "Hit or Stand?"
    in_play = True

def hit():
    global in_play, outcome, message, player, deck, score_dealer
    if not in_play:
        return
    outcome = ""
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())
    if player.get_value() > 21:
        outcome =  "You have busted and lose!"
        message = "New Deal?"
        score_dealer += 1
        in_play = False

    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score

def stand():
    global in_play, outcome, message, player, deck, dealer, score_dealer, score_player
    if not in_play:
        return
    if player.get_value() > 21:
        outcome =  "You have busted and lose!"
        return
    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())
    if dealer.get_value() > 21:
        outcome =  "Dealer has busted and you win!"
        score_player += 1
    else:
        if dealer.get_value() >= player.get_value():
            outcome =  "Dealer wins!"
            score_dealer += 1
        else:
            outcome =  "You win!"
            score_player += 1
    message = "New Deal?"
    in_play = False
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

# draw handler
def draw(canvas):
    canvas.draw_text("Blackjack", (60, 100), 40, "Aqua")
    canvas.draw_text("Dealer", (60, 185), 30, "Black")
    canvas.draw_text("Player", (60, 385), 30, "Black")
    canvas.draw_text(message, (250, 385), 25, "Black")
    canvas.draw_text(outcome, (250, 185), 30, "Black")
    canvas.draw_text("Dealer Wins: " + str(score_dealer), (350, 100), 30, "Black")
    canvas.draw_text("Player Wins: " + str(score_player), (350, 140), 30, "Black")
    dealer.draw(canvas, [20, 200])
    player.draw(canvas, [20, 400])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [20 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

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
