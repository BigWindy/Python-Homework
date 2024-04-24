#==============================================================================
#
# PROGRAM:	JoyStickCalibration
#
# PURPOSE:	Fetch data limits for the joystick and calculate the slope for
#			each segment of each axis of the joystick. Then create the
#			JoyStickData.py import file containing the data.
#
#==============================================================================

import machine
import time
import math

#==============================================================================
# -----	Constants
#==============================================================================

# -----	GPIO pins assigned to joystick

xPin = 27
yPin = 26

# -----	Empirical minimum and maximum joystick values.

xRestingLow = 0
xRestingHigh = 0
yRestingLow = 0
yRestingHigh = 0

xLowest = 0
xHighest = 0
yLowest = 0
yHighest = 0

xLowSlope = 0
xHighSlope = 0
yLowSlope = 0
yHighSlope = 0

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

def fncFetchJoyStick ():

        # -----	Since the joystick circuitry is installed horizontally reversed
        #		so the moving the joystick full left results in the highest
        #		reading and vice versa. Subtracting the X value from 65535
        #		corrects the reading (according to our definition of "correct"
     
        xVal = 65535 - xJoy.read_u16()
        yVal = yJoy.read_u16()

#        print (f'X: {xVal:6}  Y: {yVal:6}')
        
        return (xVal, yVal)

#=============================================================================
#
# Function: fncGetRestingAvg
#
# Purpose:	Get the high and low values for the joystick in a resting state
#			Grab the current (resting) values for x and y 50 times and
#			average the results
#
# Input:	None
#
# Results:	None
#
#=============================================================================

def fncGetRestingAvg ():
    
    bFirstPass = True
    
    xLow = 0
    xHigh = 0

    yLow = 0
    yHigh = 0
    
    xLowCount = 0
    xHighCount = 0

    yLowCount = 0
    yHighCount = 0

    # -----	50 times should give us a decent average
    
    for iteration in range (50):
        
        # -----	Fetch the current joystick values

        xActualVal, yActualVal = fncFetchJoyStick ()
        
        # --- Accumulate the reported values
        
        if xActualVal < xLow or bFirstPass:
            xLow += xActualVal
            xLowCount += 1
        
        if xActualVal > xHigh:
            xHigh += xActualVal
            xHighCount += 1
        
        if yActualVal < yLow or bFirstPass:
            yLow += yActualVal
            yLowCount += 1
        
        if yActualVal > yHigh:
            yHigh += yActualVal
            yHighCount += 1
        
        bFirstPass = False 
        time.sleep (.01)

    xLow = round (xLow / xLowCount)
    xHigh = round (xHigh / xHighCount)
    yLow = round (yLow / yLowCount)
    yHigh = round (yHigh / yHighCount)
    
    return (xLow, xHigh, yLow, yHigh)

#=============================================================================
#
# Function: fncGetResting
#
# Purpose:	Get the high and low values for the joystick in a resting state
#
# Input:	None
#
# Results:	None
#
#=============================================================================

def fncGetResting ():
    
    xLow = 999999
    xHigh = 0

    yLow = 999999
    yHigh = 0

    # -----	50 times should give us a decent average
    
    for iteration in range (200):
        
        # -----	Fetch the current joystick values

        xActualVal, yActualVal = fncFetchJoyStick ()
        
        # --- Accumulate the reported values
        
        if xActualVal < xLow:
            xLow = xActualVal
        
        if xActualVal > xHigh:
            xHigh = xActualVal
      
        if yActualVal < yLow:
            yLow = yActualVal
        
        if yActualVal > yHigh:
            yHigh = yActualVal
        
        time.sleep (.01)

    return (xLow, xHigh, yLow, yHigh)

#=============================================================================
#
# Function: fncGetLow
#
# Purpose:	Get the lowest value for the joystick in either the x or y position
#
# Input:	bGetX - True = Get low X, False = Get low Y
#
# Results:	Lowest reading
#
#=============================================================================

def fncGetLow (bGetX):
    
    lowVal = 999999

    # -----	100 times should give us a decent shot at seeing the lowest reading
        
    for iteration in range (100):
        
        # -----	Fetch the current joystick values

        xActualVal, yActualVal = fncFetchJoyStick ()
        
        # --- Compare the reported value
        
        if bGetX:
            if xActualVal < lowVal:
                lowVal = xActualVal
        elif yActualVal < lowVal:
                lowVal = yActualVal
            
        time.sleep (.01)

    return (lowVal)

#=============================================================================
#
# Function: fncGetHigh
#
# Purpose:	Get the highest value for the joystick in either the x or y position
#
# Input:	bGetX - True = Get high X, False = Get high Y
#
# Results:	Highest high reading
#
#=============================================================================

def fncGetHigh (bGetX):
    
    hiVal = 0

    # -----	100 times should give us a decent shot at seeing the highest reading
        
    for iteration in range (100):
        
        # -----	Fetch the current joystick values

        xActualVal, yActualVal = fncFetchJoyStick ()
        
        # --- Accumulate the reported value
        
        if bGetX:
            if xActualVal > hiVal:
                hiVal = xActualVal
        elif yActualVal < hiVal:
                hiVal = yActualVal
                
        time.sleep (.01)

    return (hiVal)

#=============================================================================
#
# Function: fncCalcSlopes
#
# Purpose:	Calculate the slope of each segment of the joystick's range.
#			Ranges are: low X, high X, Low Y, and High Y
#
# Input:	xLow - Lowest x
#			xHigh - Highest X
#			yLow - Lowest Y
#			yHigh - Highest Y
#
# Results:	low x slope, high x slope, low y slope, high y slope
#
#=============================================================================

def fncCalcSlopes (xLow, xHigh, yLow, yHigh):

    # -----	The min and max we want to see for each range

    minRange = 0
    maxRange = 100

    xLow = (maxRange - minRange) / (xLow - xRestingLow)
    xHigh = (maxRange - minRange) / (xHigh - xRestingHigh)

    yLow = (maxRange - minRange) / (yLow - yRestingLow)
    yHigh = (maxRange - minRange) / (yHigh - yRestingHigh)

    return (xLow, xHigh, yLow, yHigh)

#==============================================================================
#	Main 
#==============================================================================


# -----	Assign the device to GPIO pins

xJoy = machine.ADC (xPin)
yJoy = machine.ADC (yPin)

# -----	Do our thing

try:
    
    # -----	Get the resting state values
    
    input('Release joystick then press enter to capture resting state values')
    xRestingLow, xRestingHigh, yRestingLow, yRestingHigh = fncGetResting ()
    print (f'Resting X Low: {xRestingLow}   X High: {xRestingHigh}    Y Low: {yRestingLow}   Y High: {yRestingHigh}')

    # -----	A little advice
    
    print ('\nPlease Note:')
    print ('   The following procedures require you to move the joystick to the extremes')
    print ('   Move the joystick to the extremes as instructed then wiggle it slightly')
    print ('   back and forth. This will ensure that the joystick actually see the ')
    print ('   highest/lowest points.\n')
    
    # -----	Get the lowest X value
    
    input('\nMove joystick to the left and wiggle it. Then press enter to capture the lowest X value')
    xLowest = fncGetLow (True)
    print (f'X Low: {xLowest:10}')

    # -----	Get the highest X value
    
    input('\nMove joystick to the right and wiggle it. Then press enter to capture the highest X value')
    xHighest = fncGetHigh (True)
    print (f'X High: {xHighest:10}')

    # -----	Get the lowest Y value
    
    input('\nMove joystick to the bottom and wiggle it. Then press enter to capture the lowest Y value')
    yLowest = fncGetLow (False)
    print (f'Y Low: {yLowest:10}')

    # -----	Get the highest Y value
    
    input('\nMove joystick to the top and wiggle it. Then press enter to capture the highest Y value')
    yHighest = fncGetLow (False)
    print (f'Y High: {yHighest:10}')
    
    # -----	Let 'em off the hook
    
    print ('You may release the joystick now')
    
    xLowSlope, xHighSlope, yLowSlope, yHighSlope = fncCalcSlopes(xLowest, xHighest, yLowest, yHighest)
    
    # -----	Show off what we found
    
    print ('Readings:')
    print (f'	Lowest X:  {xLowest:>6}')
    print (f'	Highest X: {xHighest:>6}')
    print (f'	Lowest Y:  {yLowest:>6}')
    print (f'	Highest Y: {yHighest:>6}')
    
    print ('Slopes:')
    print (f'	Low X:  {xLowSlope:>12}')
    print (f'	High X: {xHighSlope:12}')
    print (f'	Low Y:  {yLowSlope:12}')
    print (f'	High Y: {yHighSlope:>12}')

    # -----	Create the output file

    fJoyStickRaw = open ('JoyStickData.py', 'wt')

    fJoyStickRaw.write('class JoyStickData:\n')

    fJoyStickRaw.write(f'	xRestingLow = {xRestingLow}\n')
    fJoyStickRaw.write(f'	xRestingHigh = {xRestingHigh}\n')
    fJoyStickRaw.write(f'	yRestingLow = {yRestingLow}\n')
    fJoyStickRaw.write(f'	yRestingHigh = {yRestingHigh}\n')

    fJoyStickRaw.write(f'\n')
    fJoyStickRaw.write(f'	xMin = {xLowest}\n')
    fJoyStickRaw.write(f'	xMax = {xHighest}\n')
    fJoyStickRaw.write(f'	yMin = {yLowest}\n')
    fJoyStickRaw.write(f'	yMax = {yHighest}\n')

    fJoyStickRaw.write(f'\n')
    fJoyStickRaw.write(f'	xLowSlope = {xLowSlope: .8}\n')
    fJoyStickRaw.write(f'	xHighSlope = {xHighSlope: .8}\n')
    fJoyStickRaw.write(f'	yLowSlope = {yLowSlope: .8}\n')
    fJoyStickRaw.write(f'	yHighSlope = {yHighSlope: .8}\n')

    fJoyStickRaw.close()
    
# --- Catch the interrupt

except KeyboardInterrupt:
    print('Good night, Mrs. Calabash, wherever you are.')
