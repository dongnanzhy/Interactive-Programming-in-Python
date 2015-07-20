# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

secret_number = 0
num_range = 100
num_remain = 0
# helper function to start and restart the game
def new_game():
    global secret_number, num_remain
    secret_number = random.randrange(0,num_range)
    num_remain = int(math.ceil(math.log(num_range, 2)))
    print "New Game Start!", "Range is from",0,"to",num_range
    print "Number of remaining guess is", num_remain
    print ""


# define event handlers for control panel
def range100():
    global num_range
    num_range = 100
    new_game()

def range1000():
    global num_range
    num_range = 1000
    new_game()

def input_guess(guess):
    global num_remain
    guess_number = int(guess)
    print "Guess was", guess_number
    if guess_number < 0 or guess_number > num_range:
        print "Invalid Input! Please type again!"
        print ""
        return

    num_remain = num_remain - 1
    print "Number of remaining guess is", num_remain

    if guess_number == secret_number:
        print "Correct"
        print ""
        new_game()
    else:
        if num_remain == 0:
            print "Game Over! You ran out of guesses! The number is", secret_number
            print ""
            new_game()
        else:
            if guess_number > secret_number:
                print "Lower"
            else:
                print "Higher"
            print ""



# create frame
frame = simplegui.create_frame("Guess the number", 300, 300)


# register event handlers for control elements and start frame
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("input_guess", input_guess, 200)

# call new_game
new_game()
