#==============================================================================
#
# PROGRAM:	JoyStick
#
# PURPOSE:	Import file containing the JoyStick class. Provides all I/O
#			functions for the JoyStick
#
#==============================================================================

import machine
import time
import JoyStickData

#==============================================================================
# -----	Global
#==============================================================================

#=============================================================================
#
# Class: 	JoyStick
#
# Purpose:	Provide all necessary functions for use of the JoyStick
#
#=============================================================================

class JoyStick:

    #=============================================================================
    #
    # Function: __init__
    #
    # Purpose:	class Initializer
    #
    # Input:	xGPIO	-	GPIO pin for the JoyStick's X axis
    #			yGPIO	-	GPIO pin for the JoyStick's Y axis
    #
    # Results:	None
    #
    #=============================================================================
    
    def __init__(self, xGPIO, yGPIO):

        #==============================================================================
        #	Assign the device to GPIO pins
        #==============================================================================

        self.xJoy = machine.ADC (xGPIO)
        self.yJoy = machine.ADC (yGPIO)

        #==============================================================================
        #	Create the joystick object
        #==============================================================================

        self.js = JoyStickData.JoyStickData ()

    #=============================================================================
    #
    # Function: fncFetchJoyStickRaw
    #
    # Purpose:	Fetch the raw JoyStick values
    #
    # Input:	None
    #
    # Results:	xVal, yVal
    #
    #=============================================================================

    def fncFetchJoyStickRaw (self):
        
        xVal = self.xJoy.read_u16()
        yVal = self.yJoy.read_u16()
        
        return (xVal, yVal)

    #=============================================================================
    #
    # Function: fncFetchJoyStick
    #
    # Purpose:	Fetch the JoyStick values
    #
    # Input:	None
    #
    # Results:	xVal, yVal
    #
    #=============================================================================

    def fncFetchJoyStick (self):
        
        # -----	Fetch the joystick reading
        
        xRawVal, yRawVal = self.fncFetchJoyStickRaw ()

        # -----	Since the joystick circuitry is installed horizontally reversed
        #		so the moving the joystick full left results in the highest
        #		reading and vice versa. Subtracting the X value from 65535
        #		corrects the reading (according to our definition of "correct"
        
        xRawVal = 65535 - xRawVal
        
        # --- Convert the adjusted values a value within our range
        
        if xRawVal < self.js.xRestingLow:
            xVal = round (self.js.xLowSlope * (self.js.xRestingLow - xRawVal))
        elif xRawVal > self.js.xRestingHigh:
            xVal = round (self.js.xHighSlope * (xRawVal - self.js.xRestingHigh))
        else:
            xVal = 0
        
        if yRawVal < self.js.yRestingLow:
            yVal = round (self.js.yLowSlope * (self.js.yRestingLow - yRawVal))
        elif yRawVal > self.js.yRestingHigh:
            yVal = round (self.js.yHighSlope * (yRawVal - self.js.yRestingHigh))
        else:
            yVal = 0
        
        return (xVal, yVal)
