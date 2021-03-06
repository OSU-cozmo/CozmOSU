import cozmo
import math

"""
RGB to Light (color)
    Purpose : create a light object that the cozmo library uses
    Parameters: Color -> tuple, in form (r, g, b)
"""
def rgbToLight(color : tuple):
    #Create cozmo color object
    c = cozmo.lights.Color(rgb = color)

    #return a light made using that color
    return cozmo.lights.Light(on_color = c)

"""
Hex to RGB (color)
    Purpose: convert a hex string into an rgb tuple
    Parameters: color -> string, in form '0xFFF' or '0xFFFFFF'
"""
def hexToRBG(color):

    #drop the 0x from the front of the string
    if "0x" in color[:2]:
        color = color[2:]

    #check that the string is 3 or 6 chars long
    if len(color) not in [3,6]:
        return None

    #step is lenhth divided by 3
    #   1 or 2
    step = len(color) // 3

    #convert to an int, using base 16 conversion
    #Clamp to 0 - 256

    #0 to step is the red value
    red = int(color[:step], 16) % 256

    #step to step * 2 is the green value
    green = int(color[step:step+step], 16) % 256

    #step * 2 to the end is the blue value
    blue = int(color[step+step:], 16) % 256

    #Create the tuple, then return
    return (red, green, blue)

"""
Build Gradient (indexes, color1, color2)
    Purpose : Create an array of colors (gradient)
    Parameters: indexes -> int, how many colors to generate between the two colors
                color1 -> tuple, rgb start color
                color2 -> tuple, rgb end color
"""
def buildGradient(indexes : int, color1 : tuple, color2 : tuple):
    #create colors array
    colors = []
    #Convert both colors to HSV
    color1 = rgbToHSV(color1)
    color2 = rgbToHSV(color2)

    #Get the difference of the hue values from HSV
    dif = abs(color2[0] - color1[0])

    #set flip flag to false
    flip = False

    #if the difference is greater than the total  range 360/2
    if dif > 180:
        dif = dif / 2
        flip = True

    #calculate step difference / indexes
    hStep = dif / indexes

    #cannot change tuples, so cast to list
    temp = list(color1)

    #store first color in the lsit
    colors.append(color1)

    for x in range(1, indexes-1):

        #add or sub step based off of direction dictated by the flag
        #mod 360 so that it will warp back to 0
        if flip:
            temp[0] = (temp[0] - hStep) % 360
        else:
            temp[0] = (temp[0] + hStep) % 360

        #cast to tuple, then append
        colors.append(tuple(temp))

    #append the last color
    colors.append(color2)

    #convert all colors in the list to RGB then return
    return list(map(hsvToRGB, colors))


def rgbToHSV(color : tuple):
    #referenced http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/

    r = color[0] / 255
    g = color[1] / 255
    b = color[2] / 255

    maxC = max(r, g, b)
    minC = min(r, g, b)

    dF = maxC - minC
    h, s, l = 0, 0, 0

    if max is min:
        h = 0
    elif maxC is r:
        h = (60 * ((g - b) / dF) + 360) % 360
    elif maxC is g:
        h = (60 * ((b - r) / dF) + 120) % 360
    elif maxC is b:
        h = (60 * ((r - g) / dF) + 240) % 360

    if maxC is not 0:
        s = dF / maxC
    v = maxC
    return (h, s, v)


def hsvToRGB(color : tuple):
    #referenced http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
    h = float(color[0])
    s = float(color[1])
    v = float(color[2])

    h60 = h / 60
    h60Floor = math.floor(h60)
    hi = int(h60Floor) % 6

    f = h60 - h60Floor
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r, g, b = 0, 0, 0

    if hi is 0:
        r, g, b = v, t, p
    elif hi is 1:
        r, g, b = q, v, p
    elif hi is 2:
        r, g, b = p, v, t
    elif hi is 3:
        r, g, b = p, q, v
    elif hi is 4:
        r, g, b = t, p, v
    elif hi is 5:
        r, g, b = v, p, q

    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return(r, g, b)
