#==============================================================================
#
# PROGRAM:	Lesson 56
#
# PURPOSE:	Fetch and display position readings from Joystick 
#
#==============================================================================

import machine
import time
import JoyStick

#==============================================================================
# -----	Constants
#==============================================================================

# -----	GPIO pins assigned to joystick

xPin = 27
yPin = 26

#==============================================================================
#	Main 
#==============================================================================

try:
    
    # -----	Create the JoyStick object
    
    JoyS = JoyStick.JoyStick (xPin, yPin)
    
    while True:
        
        xVal, yVal = JoyS.fncFetchJoyStick ()
        
        print (f'X: {xVal:4}  Y: {yVal:4}')
        
        time.sleep (.1)
    
# --- Catch the interrupt

except KeyboardInterrupt:
    print('Good night, Mrs. Calabash, wherever you are.')
    
# --- Turn out the lights. The party's over.
