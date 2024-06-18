import time 
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import rotaryio                           #rotary encoder library for mouse encoder wheels
from adafruit_debouncer import Debouncer  #debounce library for input switches

#mouse buttons - need to add right click
mouseLeftClick = DigitalInOut(board.GP22)
mouseLeftClick.direction = Direction.INPUT
mouseLeftClick.pull = Pull.UP

#init usb keyboard/mouse interfaces
time.sleep(1)  # sleep for a while to avoid a race condition on some systems (saw this done somewhere, unsure if needed)
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
mouseLeftClick_state = None

#set up a rotary encoder interface to monitor encoder discs on each mouse axis input 
x_axis1 = rotaryio.IncrementalEncoder(board.GP0, board.GP1)
y_axis1 = rotaryio.IncrementalEncoder(board.GP2, board.GP3)
x_axis2 = rotaryio.IncrementalEncoder(board.GP4, board.GP5)
y_axis2 = rotaryio.IncrementalEncoder(board.GP6, board.GP7)
x_axis3 = rotaryio.IncrementalEncoder(board.GP8, board.GP9)
y_axis3 = rotaryio.IncrementalEncoder(board.GP10, board.GP11)

#initial conditions for mouse position tracking: previous and current positions assumed to be the same (not moving)
last_x_axis1_position = x_axis1.position
last_y_axis1_position = y_axis1.position
last_x_axis2_position = x_axis2.position
last_y_axis2_position = y_axis2.position
last_x_axis3_position = x_axis3.position
last_y_axis3_position = y_axis3.position

dbInterval = 0.03           #30 mS debounce for switch inputs
keypress_hold_delay = 0.11  #duration (seconds) to hold down usb keyboard key presses before releasing

#configure debounced switch inputs for the four inputs (a, b, c, d) on rotary joystick 1 and 2
rotary1a = DigitalInOut(board.GP20)
rotary1a.direction = Direction.INPUT
rotary1a.pull = Pull.UP
rotary1a_DB = Debouncer(rotary1a, interval=dbInterval)

rotary1b = DigitalInOut(board.GP19)
rotary1b.direction = Direction.INPUT
rotary1b.pull = Pull.UP
rotary1b_DB = Debouncer(rotary1b, interval=dbInterval)

rotary1c = DigitalInOut(board.GP18)
rotary1c.direction = Direction.INPUT
rotary1c.pull = Pull.UP
rotary1c_DB = Debouncer(rotary1c, interval=dbInterval)

rotary1d = DigitalInOut(board.GP17)
rotary1d.direction = Direction.INPUT
rotary1d.pull = Pull.UP
rotary1d_DB = Debouncer(rotary1d, interval=dbInterval)

rotary2a = DigitalInOut(board.GP16)
rotary2a.direction = Direction.INPUT
rotary2a.pull = Pull.UP
rotary2a_DB = Debouncer(rotary2a, interval=dbInterval)

rotary2b = DigitalInOut(board.GP14)
rotary2b.direction = Direction.INPUT
rotary2b.pull = Pull.UP
rotary2b_DB = Debouncer(rotary2b, interval=dbInterval)

rotary2c = DigitalInOut(board.GP13)
rotary2c.direction = Direction.INPUT
rotary2c.pull = Pull.UP
rotary2c_DB = Debouncer(rotary2c, interval=dbInterval)

rotary2d = DigitalInOut(board.GP12)
rotary2d.direction = Direction.INPUT
rotary2d.pull = Pull.UP
rotary2d_DB = Debouncer(rotary2d, interval=dbInterval)

#read current debounced state of rotary joystick 1 switches
def readDebouncedRotary1():    
    rotaryReading = 0

    rotary1a_DB.update() 
    if rotary1a_DB.value == 0:
        rotaryReading = rotaryReading | 1    

    rotary1b_DB.update() 
    if rotary1b_DB.value == 0:
        rotaryReading = rotaryReading | 1<<1  

    rotary1c_DB.update() 
    if rotary1c_DB.value == 0:
        rotaryReading = rotaryReading | 1<<2    

    rotary1d_DB.update() 
    if rotary1d_DB.value == 0:
        rotaryReading = rotaryReading | 1<<3    

    return rotaryReading

#read current state of rotary joystick 2 switches
def readDebouncedRotary2():    
    rotaryReading = 0

    rotary2a_DB.update() 
    if rotary2a_DB.value == 0:
        rotaryReading = rotaryReading | 1    

    rotary2b_DB.update() 
    if rotary2b_DB.value == 0:
        rotaryReading = rotaryReading | 1<<1  

    rotary2c_DB.update() 
    if rotary2c_DB.value == 0:
        rotaryReading = rotaryReading | 1<<2    

    rotary2d_DB.update() 
    if rotary2d_DB.value == 0:
        rotaryReading = rotaryReading | 1<<3    

    return rotaryReading

#update rotary 1 switches, looking for edge transitions to indicate new movement
#returns -1 if no movement has occurred since last reading
def readRotary1():
    
    rotary1a_DB.update() 
    if rotary1a_DB.fell:
        rotaryReading = 0
        rotaryReading = rotaryReading | 1    
        return rotaryReading

    rotary1b_DB.update() 
    if rotary1b_DB.fell:
        rotaryReading = 0
        rotaryReading = rotaryReading | 1<<1  
        return rotaryReading

    rotary1c_DB.update() 
    if rotary1c_DB.fell:
        rotaryReading = 0
        rotaryReading = rotaryReading | 1<<2 
        return rotaryReading   

    rotary1d_DB.update() 
    if rotary1d_DB.fell:
        rotaryReading = 0
        rotaryReading = rotaryReading | 1<<3
        return rotaryReading   

    return -1 

#update rotary 2 switches, looking for edge transitions to indicate new movement
#returns -1 if no movement has occurred since last reading
def readRotary2():
    
    rotary2a_DB.update() 
    if rotary2a_DB.fell:
        rotaryReading = 0
        rotaryReading = rotaryReading | 1    
        return rotaryReading

    rotary2b_DB.update() 
    if rotary2b_DB.fell:
        rotaryReading = 0
        rotaryReading = rotaryReading | 1<<1  
        return rotaryReading

    rotary2c_DB.update() 
    if rotary2c_DB.fell:
        rotaryReading = 0
        rotaryReading = rotaryReading | 1<<2 
        return rotaryReading   

    rotary2d_DB.update() 
    if rotary2d_DB.fell:
        rotaryReading = 0
        rotaryReading = rotaryReading | 1<<3
        return rotaryReading   

    return -1 

#set last joystick position to current debounced position for initial conditions
rotary1_now = readDebouncedRotary1()
rotary2_now = readDebouncedRotary2()
rotary1_last = rotary1_now
rotary2_last = rotary2_now

#main loop
while True:

#rotary joystick processing
    #check if movement has occurred since last reading and set a bit to show the current joystick position
    #if no movement is detected, the rotary[1,2]_now variables are not updated, holding their previous values 
    reading1 = readRotary1()
    reading2 = readRotary2()
    if reading1 > 0:
       rotary1_now = reading1
    if reading2 > 0:
       rotary2_now = reading2

    #debug printout
    #print ("rotary1_now: %16s" %(bin(rotary1_now)))
    #print ("rotary2_now: %16s" %(bin(rotary2_now)))

    #check if joysticks have rotated by comparing the last valid state against the most recent reading
    diff1 = (rotary1_last - rotary1_now)   
    diff2 = (rotary2_last - rotary2_now)
 
    #joystick 1 clockwise rotation has occurred
    if ( ((diff1 < 0) and not ((rotary1_last == 0b0001) and (rotary1_now == 0b1000)) ) or ((diff1 > 0) and (rotary1_last == 0b1000) and (rotary1_now == 0b0001))): 
        #send keystroke
        kbd.press(Keycode.X)
        time.sleep(keypress_hold_delay)
        kbd.release_all()
        #print ("rotary1_now: %16s" %(bin(rotary1_now)))   #movement has occurred
        #print ("CW")

    #joystick 1 counter-clockwise rotation has occurred
    if ( ((diff1 > 0) and not ((rotary1_last == 0b1000) and (rotary1_now == 0b0001)) ) or ((diff1 < 0) and (rotary1_last == 0b0001) and (rotary1_now == 0b1000))): 
        #send keystroke 
        kbd.press(Keycode.Z)
        time.sleep(keypress_hold_delay)
        kbd.release_all()
        #print ("rotary1_now: %16s" %(bin(rotary1_now)))   #movement has occurred
        #print ("CCW")

    if not diff1 == 0:
        rotary1_last = rotary1_now   # update previous saved joystick position if movement has occurred

    #joystick 2 clockwise rotation has occurred
    if ( ((diff2 < 0) and not ((rotary2_last == 0b0001) and (rotary2_now == 0b1000)) ) or ((diff2 > 0) and (rotary2_last == 0b1000) and (rotary2_now == 0b0001))): 
        #send keystroke 
        kbd.press(Keycode.F)
        time.sleep(keypress_hold_delay)
        kbd.release_all()
        #print ("rotary2_now: %16s" %(bin(rotary2_now)))   #movement has occurred
        #print ("CW")

    #joystick 2 counter-clockwise rotation has occurred
    if ( ((diff2 > 0) and not ((rotary2_last == 0b1000) and (rotary2_now == 0b0001)) ) or ((diff2 < 0) and (rotary2_last == 0b0001) and (rotary2_now == 0b1000))): 
        #send keystroke 
        kbd.press(Keycode.B)
        time.sleep(keypress_hold_delay)
        kbd.release_all()
        #print ("rotary2_now: %16s" %(bin(rotary2_now)))   #movement has occurred
        #print ("CCW")

    if not diff2 == 0:
        rotary2_last = rotary2_now    # update previous saved joystick position if movement has occurred

#mouse buttons, work in progress
    if not mouseLeftClick.value and mouseLeftClick_state is None:
        mouseLeftClick_state = "pressed"
    if mouseLeftClick.value and mouseLeftClick_state == "pressed":
        print("Left mouse button pressed.")
        mouseLeftClick_state = None

    #mouse movement variables
    slowMovementInc = 5       #amount to move cursor when slow
    fastMovementInc = 20      #amount to move cursor when fast
    accelThreshold = 5        #amount of cursor position change to be considered moving fast

#X_Axis 1
    current_x_axis1_position = x_axis1.position
    position_change_x_axis1 = current_x_axis1_position - last_x_axis1_position
    if position_change_x_axis1 > 0 and position_change_x_axis1 < accelThreshold:     #move mouse to the right, slowly
            mouse.move(x=position_change_x_axis1+slowMovementInc)
    elif position_change_x_axis1 >= accelThreshold:                                  #move mouse to the right, faster
            mouse.move(x=fastMovementInc)
    elif position_change_x_axis1 < 0 and position_change_x_axis1 > -accelThreshold:  #move mouse to the left, slowly
            mouse.move(x=position_change_x_axis1-slowMovementInc)
    elif position_change_x_axis1 <= -accelThreshold:
            mouse.move(x=-fastMovementInc)                                           #move mouse to the left, faster 
    last_x_axis1_position = current_x_axis1_position
#Y_Axis 1
    current_y_axis1_position = y_axis1.position
    position_change_y_axis1 = current_y_axis1_position - last_y_axis1_position
    if position_change_y_axis1 > 0 and position_change_y_axis1 < accelThreshold:     #move mouse up, slowly
            mouse.move(y=position_change_y_axis1+slowMovementInc)
    elif position_change_y_axis1 >= accelThreshold:                                  #move mouse up, faster
            mouse.move(y=fastMovementInc)
    elif position_change_y_axis1 < 0 and position_change_y_axis1 > -accelThreshold:  #move mouse down, slowly
            mouse.move(y=position_change_y_axis1-slowMovementInc)
    elif position_change_y_axis1 <= -accelThreshold:                                 #move mouse down, faster
            mouse.move(y=-fastMovementInc)
    last_y_axis1_position = current_y_axis1_position


#X_Axis 2
    current_x_axis2_position = x_axis2.position
    position_change_x_axis2 = current_x_axis2_position - last_x_axis2_position
    if position_change_x_axis2 > 0 and position_change_x_axis2 < accelThreshold:     #move mouse to the right, slowly
            mouse.move(x=position_change_x_axis2+slowMovementInc)
    elif position_change_x_axis2 >= accelThreshold:                                  #move mouse to the right, faster
            mouse.move(x=fastMovementInc)
    elif position_change_x_axis2 < 0 and position_change_x_axis2 > -accelThreshold:  #move mouse to the left, slowly
            mouse.move(x=position_change_x_axis2-slowMovementInc)
    elif position_change_x_axis2 <= -accelThreshold:
            mouse.move(x=-fastMovementInc)                                           #move mouse to the left, faster 
    last_x_axis2_position = current_x_axis2_position
#Y_Axis 2
    current_y_axis2_position = y_axis2.position
    position_change_y_axis2 = current_y_axis2_position - last_y_axis2_position
    if position_change_y_axis2 > 0 and position_change_y_axis2 < accelThreshold:     #move mouse up, slowly
            mouse.move(y=position_change_y_axis2+slowMovementInc)
    elif position_change_y_axis2 >= accelThreshold:                                  #move mouse up, faster
            mouse.move(y=fastMovementInc)
    elif position_change_y_axis2 < 0 and position_change_y_axis2 > -accelThreshold:  #move mouse down, slowly
            mouse.move(y=position_change_y_axis2-slowMovementInc)
    elif position_change_y_axis2 <= -accelThreshold:                                 #move mouse down, faster
            mouse.move(y=-fastMovementInc)
    last_y_axis2_position = current_y_axis2_position

#X_Axis 3
    current_x_axis3_position = x_axis3.position
    position_change_x_axis3 = current_x_axis3_position - last_x_axis3_position
    if position_change_x_axis3 > 0 and position_change_x_axis3 < accelThreshold:     #move mouse to the right, slowly
            mouse.move(x=position_change_x_axis3+slowMovementInc)
    elif position_change_x_axis3 >= accelThreshold:                                  #move mouse to the right, faster
            mouse.move(x=fastMovementInc)
    elif position_change_x_axis3 < 0 and position_change_x_axis3 > -accelThreshold:  #move mouse to the left, slowly
            mouse.move(x=position_change_x_axis3-slowMovementInc)
    elif position_change_x_axis3 <= -accelThreshold:
            mouse.move(x=-fastMovementInc)                                           #move mouse to the left, faster 
    last_x_axis3_position = current_x_axis3_position
#Y_Axis 3
    current_y_axis3_position = y_axis3.position
    position_change_y_axis3 = current_y_axis3_position - last_y_axis3_position
    if position_change_y_axis3 > 0 and position_change_y_axis3 < accelThreshold:     #move mouse up, slowly
            mouse.move(y=position_change_y_axis3+slowMovementInc)
    elif position_change_y_axis3 >= accelThreshold:                                  #move mouse up, faster
            mouse.move(y=fastMovementInc)
    elif position_change_y_axis3 < 0 and position_change_y_axis3 > -accelThreshold:  #move mouse down, slowly
            mouse.move(y=position_change_y_axis3-slowMovementInc)
    elif position_change_y_axis3 <= -accelThreshold:                                 #move mouse down, faster
            mouse.move(y=-fastMovementInc)
    last_y_axis3_position = current_y_axis3_position
