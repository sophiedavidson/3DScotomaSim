"""
file: dataManagement.py
name: Sophie Davidson
company:IMT Atlantique
date: 1/2023

    This module contains the functions required to modify and alter the eyetracking data before it is displayed to the
    screen

"""


# Moves the scotoma to a relative location.
def transformEyeData(thisX, thisY, location):
    if location == "N":
        thisY = thisY - 50
    elif location == "NE":
        thisX = thisX + 50
        thisY = thisY - 50
    elif location == "E":
        thisX = thisX + 50
    elif location == "SE":
        thisX = thisX + 50
        thisY = thisY + 50
    elif location == "S":
        thisY = thisY + 50
    elif location == "SW":
        thisX = thisX - 50
        thisY = thisY + 50
    elif location == "W":
        thisX = thisX - 50
    elif location == "NW":
        thisX = thisX - 50
        thisY = thisY - 50
    return thisX, thisY
