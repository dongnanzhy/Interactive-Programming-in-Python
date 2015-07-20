import simplegui

# define global variables
position = [120,200]
width = 400
height = 400
interval = 100
num_time = 0
num_success = 0
num_stops = 0
message = "0/0"

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(num):
    t = num
    tenthSec = t%10
    t = t/10
    sec_unit = t%10
    t = t/10
    sec_ten = t%6
    minute = t/6
    return str(minute)+":"+str(sec_ten)+str(sec_unit)+"."+str(tenthSec)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    if timer.is_running():
        timer.stop()
        global num_success, num_stops, message
        num_stops += 1
        if (num_time % 10 == 0):
            num_success += 1
        message = str(num_success)+"/"+str(num_stops)

def reset():
    global num_time, num_success, num_stops, message
    timer.stop()
    num_time = 0
    num_success = 0
    num_stops = 0
    message = "0/0"

# define event handler for timer with 0.1 sec interval
def tick():
    global num_time, message
    num_time = num_time + 1


# define draw handler
def draw (canvas):
    canvas.draw_text(format(num_time), position, 70, "White")
    canvas.draw_text(message, [300,50], 50, "Red")

# create frame
frame = simplegui.create_frame("Stopwatch",width, height)

# register event handlers
frame.add_button("Start",start,200)
frame.add_button("Stop",stop,200)
frame.add_button("Reset",reset,200)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)

# start frame
frame.start()
#timer.start()

# Please remember to review the grading rubric
