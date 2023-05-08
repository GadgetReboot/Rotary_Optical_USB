import time 
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer  #debounce library for input switches

#init usb keyboard/mouse interfaces
time.sleep(1)  # sleep for a while to avoid a race condition on some systems (saw this done somewhere, unsure if needed)
kbd = Keyboard(usb_hid.devices)

dbInterval = 0.03           #30 mS debounce for rotary joystick switch inputs
keypress_hold_delay = 0.11  #duration (seconds) to hold down usb keyboard key presses before releasing for joystick rotations

button_dbInterval = 0.03           #30 mS debounce for button inputs
button_keypress_hold_delay = 0.11  #duration (seconds) to hold down usb keyboard key presses before releasing for buttons

#assign all screw terminal inputs as digital inputs for testing (assigning to keyboard keys)
button1 = DigitalInOut(board.GP0)
button1.direction = Direction.INPUT
button1.pull = Pull.UP
button1_DB = Debouncer(button1, interval=button_dbInterval)

button2 = DigitalInOut(board.GP1)
button2.direction = Direction.INPUT
button2.pull = Pull.UP
button2_DB = Debouncer(button2, interval=button_dbInterval)

button3 = DigitalInOut(board.GP2)
button3.direction = Direction.INPUT
button3.pull = Pull.UP
button3_DB = Debouncer(button3, interval=button_dbInterval)

button4 = DigitalInOut(board.GP3)
button4.direction = Direction.INPUT
button4.pull = Pull.UP
button4_DB = Debouncer(button4, interval=button_dbInterval)

button5 = DigitalInOut(board.GP4)
button5.direction = Direction.INPUT
button5.pull = Pull.UP
button5_DB = Debouncer(button5, interval=button_dbInterval)

button6 = DigitalInOut(board.GP5)
button6.direction = Direction.INPUT
button6.pull = Pull.UP
button6_DB = Debouncer(button6, interval=button_dbInterval)

button7 = DigitalInOut(board.GP6)
button7.direction = Direction.INPUT
button7.pull = Pull.UP
button7_DB = Debouncer(button7, interval=button_dbInterval)

button8 = DigitalInOut(board.GP7)
button8.direction = Direction.INPUT
button8.pull = Pull.UP
button8_DB = Debouncer(button8, interval=button_dbInterval)

button9 = DigitalInOut(board.GP8)
button9.direction = Direction.INPUT
button9.pull = Pull.UP
button9_DB = Debouncer(button9, interval=button_dbInterval)

button10 = DigitalInOut(board.GP9)
button10.direction = Direction.INPUT
button10.pull = Pull.UP
button10_DB = Debouncer(button10, interval=button_dbInterval)

button11 = DigitalInOut(board.GP10)
button11.direction = Direction.INPUT
button11.pull = Pull.UP
button11_DB = Debouncer(button11, interval=button_dbInterval)

button12 = DigitalInOut(board.GP11)
button12.direction = Direction.INPUT
button12.pull = Pull.UP
button12_DB = Debouncer(button12, interval=button_dbInterval)

button13 = DigitalInOut(board.GP21)
button13.direction = Direction.INPUT
button13.pull = Pull.UP
button13_DB = Debouncer(button13, interval=button_dbInterval)

button14 = DigitalInOut(board.GP22)
button14.direction = Direction.INPUT
button14.pull = Pull.UP
button14_DB = Debouncer(button14, interval=button_dbInterval)

button15 = DigitalInOut(board.GP26)
button15.direction = Direction.INPUT
button15.pull = Pull.UP
button15_DB = Debouncer(button15, interval=button_dbInterval)

button16 = DigitalInOut(board.GP27)
button16.direction = Direction.INPUT
button16.pull = Pull.UP
button16_DB = Debouncer(button16, interval=button_dbInterval)

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
        kbd.release(Keycode.X)
        #print ("rotary1_now: %16s" %(bin(rotary1_now)))   #movement has occurred
        #print ("CW")

    #joystick 1 counter-clockwise rotation has occurred
    if ( ((diff1 > 0) and not ((rotary1_last == 0b1000) and (rotary1_now == 0b0001)) ) or ((diff1 < 0) and (rotary1_last == 0b0001) and (rotary1_now == 0b1000))): 
        #send keystroke 
        kbd.press(Keycode.Z)
        time.sleep(keypress_hold_delay)
        kbd.release(Keycode.Z)
        #print ("rotary1_now: %16s" %(bin(rotary1_now)))   #movement has occurred
        #print ("CCW")

    if not diff1 == 0:
        rotary1_last = rotary1_now   # update previous saved joystick position if movement has occurred

    #joystick 2 clockwise rotation has occurred
    if ( ((diff2 < 0) and not ((rotary2_last == 0b0001) and (rotary2_now == 0b1000)) ) or ((diff2 > 0) and (rotary2_last == 0b1000) and (rotary2_now == 0b0001))): 
        #send keystroke 
        kbd.press(Keycode.F)
        time.sleep(keypress_hold_delay)
        kbd.release(Keycode.F)
        #print ("rotary2_now: %16s" %(bin(rotary2_now)))   #movement has occurred
        #print ("CW")

    #joystick 2 counter-clockwise rotation has occurred
    if ( ((diff2 > 0) and not ((rotary2_last == 0b1000) and (rotary2_now == 0b0001)) ) or ((diff2 < 0) and (rotary2_last == 0b0001) and (rotary2_now == 0b1000))): 
        #send keystroke 
        kbd.press(Keycode.B)
        time.sleep(keypress_hold_delay)
        kbd.release(Keycode.B)
        #print ("rotary2_now: %16s" %(bin(rotary2_now)))   #movement has occurred
        #print ("CCW")

    if not diff2 == 0:
        rotary2_last = rotary2_now    # update previous saved joystick position if movement has occurred

#check screw terminals for button presses and send a keyboard keypress
    button1_DB.update() 
    if button1_DB.fell:
        kbd.press(Keycode.G)
        #time.sleep(button_keypress_hold_delay)
    if button1_DB.rose:
        kbd.release(Keycode.G)

    button2_DB.update() 
    if button2_DB.fell:
        kbd.press(Keycode.H)
        #time.sleep(button_keypress_hold_delay)
    if button2_DB.rose:
        kbd.release(Keycode.H)

    button3_DB.update() 
    if button3_DB.fell:
        kbd.press(Keycode.I)
        #time.sleep(button_keypress_hold_delay)
    if button3_DB.rose:
        kbd.release(Keycode.I)

    button4_DB.update() 
    if button4_DB.fell:
        kbd.press(Keycode.J)
        #time.sleep(button_keypress_hold_delay)
    if button4_DB.rose:
        kbd.release(Keycode.J)

    button5_DB.update() 
    if button5_DB.fell:
        kbd.press(Keycode.K)
        #time.sleep(button_keypress_hold_delay)
    if button5_DB.rose:
        kbd.release(Keycode.K)

    button6_DB.update() 
    if button6_DB.fell:
        kbd.press(Keycode.L)
        #time.sleep(button_keypress_hold_delay)
    if button6_DB.rose:
        kbd.release(Keycode.L)

    button7_DB.update() 
    if button7_DB.fell:
        kbd.press(Keycode.M)
        #time.sleep(button_keypress_hold_delay)
    if button7_DB.rose:
        kbd.release(Keycode.M)

    button8_DB.update() 
    if button8_DB.fell:
        kbd.press(Keycode.N)
        #time.sleep(button_keypress_hold_delay)
    if button8_DB.rose:
        kbd.release(Keycode.N)

    button9_DB.update() 
    if button9_DB.fell:
        kbd.press(Keycode.O)
        #time.sleep(button_keypress_hold_delay)
    if button9_DB.rose:
        kbd.release(Keycode.O)

    button10_DB.update() 
    if button10_DB.fell:
        kbd.press(Keycode.P)
        #time.sleep(button_keypress_hold_delay)
    if button10_DB.rose:
        kbd.release(Keycode.P)

    button11_DB.update() 
    if button11_DB.fell:
        kbd.press(Keycode.Q)
        #time.sleep(button_keypress_hold_delay)
    if button11_DB.rose:
        kbd.release(Keycode.Q)

    button12_DB.update() 
    if button12_DB.fell:
        kbd.press(Keycode.R)
        #time.sleep(button_keypress_hold_delay)
    if button12_DB.rose:
        kbd.release(Keycode.R)

    button13_DB.update() 
    if button13_DB.fell:
        kbd.press(Keycode.S)
        #time.sleep(button_keypress_hold_delay)
    if button13_DB.rose:
        kbd.release(Keycode.S)

    button14_DB.update() 
    if button14_DB.fell:
        kbd.press(Keycode.T)
        #time.sleep(button_keypress_hold_delay)
    if button14_DB.rose:
        kbd.release(Keycode.T)

    button15_DB.update() 
    if button15_DB.fell:
        kbd.press(Keycode.U)
        #time.sleep(button_keypress_hold_delay)
    if button15_DB.rose:
        kbd.release(Keycode.U)

    button16_DB.update() 
    if button16_DB.fell:
        kbd.press(Keycode.V)
        #time.sleep(button_keypress_hold_delay)
    if button16_DB.rose:
        kbd.release(Keycode.V)