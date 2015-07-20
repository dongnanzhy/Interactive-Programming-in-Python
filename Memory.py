# implementation of card game - Memory

import simplegui
import random

#CAN_WIDTH = 800
#CAN_HEIGHT = 100
deck = range(8) + range(8)
exposed = [False]*16
state = 0
index_turn = [0,0]
count = 0

# helper function to initialize globals
def new_game():
    global deck, exposed, state, count
    random.shuffle(deck)
    exposed = [False for tag in exposed]
    state = 0
    count = 0

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, index_turn, count
    index = list(pos)[0]//50
    if not exposed[index]:
        exposed[index] = True
        if state == 0:
            index_turn[0] = index
            state = 1
        elif state == 1:
            count = count + 1
            index_turn[1] = index
            state = 2
        else:
            state = 1
            if deck[index_turn[0]] != deck[index_turn[1]]:
                exposed[index_turn[0]] = False
                exposed[index_turn[1]] = False
            index_turn[0] = index

# cards are logically 50x100 pixels in size
def draw(canvas):
    for i in range(16):
        if exposed[i]:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "Red", "Black")
            canvas.draw_text(str(deck[i]), (i*50+15, 60), 40, "White")
        else:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "Red", "Green")
    label.set_text("Turns = " + str(count))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
