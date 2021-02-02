#!/usr/bin/env python3

# Imports
import time
import rpi_ws281x
import argparse
from gpiozero import Button
import calendar
import datetime
from enum import Enum
import json

# LED strip configuration.
LED_COUNT = 42        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 8    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Other Constants
HABIT_DATA_FILE = "habit-data.json"

# Color Enum for easy color references.
class Color(Enum):
    BLANK = rpi_ws281x.Color(0,0,0)
    RED = rpi_ws281x.Color(255,0,0)
    GREEN = rpi_ws281x.Color(0, 255, 0)
    BLUE = rpi_ws281x.Color(0, 0, 255)
    WHITE = rpi_ws281x.Color(255, 255, 255)

# LED array representing the colors of the display.
leds = [Color.BLANK] * LED_COUNT

# Initialize the Strip of LEDS.
strip = rpi_ws281x.PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Currently selected day.
selectedDay = datetime.datetime.now()

# Habit tracker data in JSON format.
habitData = None

# Clears LEDs colors.
def clearLeds():
    global leds
    leds = [Color.BLANK] * LED_COUNT

# Display the led colors on the strip.
def displayLeds():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, leds[i].value)
    strip.show()

def drawMonth():
    clearLeds()

    offset = getOffsetOfMonth(selectedDay.year, selectedDay.month)
    days = getDaysOfMonth(selectedDay.year, selectedDay.month)
    
    for i in range(offset, days + offset):
        leds[i] = Color.WHITE
    
    displayLeds()

# Returns the total number of days in the given month.
def getDaysOfMonth(year, month):
    return calendar.monthrange(year, month)[1]

# Returns the weekday offset of the month. Sunday is 0, Saturday is 6. (i.e. if the month starts on a tuesday, return 2.)
def getOffsetOfMonth(year, month):
    # Python considers Monday as day 0, so shift weekday value up by one, looping back to 0 in the case of Sunday.
    return calendar.monthrange(selectedDay.year, selectedDay.month)[0] + 1 % 7

# Lights up red, green, and blue LEDs in order.
def testDisplay(intervalTimeMs=50, waitTimeMs=1000):
    primaries = [Color.RED, Color.GREEN, Color.BLUE]
    for primary in primaries:
        for i in range(strip.numPixels()):
            leds[i] = primary
            displayLeds()
            time.sleep(intervalTimeMs/1000)
    time.sleep(waitTimeMs/1000)
    clearLeds()
    displayLeds()

# Sets selectedDay to the current local day.
def setSelectedDayToNow():
    global selectedDay
    selectedDay = datetime.datetime.now()

# Shifts selectedDay by the delta number of days.
def shiftSelectedDay(delta):
    global selectedDay
    selectedDay += datetime.timedelta(days=delta)

def readHabitData():
    global habitData
    try:
        with open(HABIT_DATA_FILE, mode="r", encoding="utf-8") as file:
            habitData = json.load(file)
    except OSError:
        print("OSError: Unable to open file " + HABIT_DATA_FILE, flush=True)

def writeHabitData():
    try:
        with open(HABIT_DATA_FILE, mode="w", encoding="utf-8") as file:
            json.dump(habitData, file)
    except OSError:
        print("OSError: Unable to open file " + HABIT_DATA_FILE, flush=True)
    

def main():
    try:
        readHabitData()

        drawMonth()
        shiftSelectedDay(-1)
        drawMonth()

    except KeyboardInterrupt:
        clearLeds()
        displayLeds()

    # testDisplay()


    # Set up GPIO buttons.
    # buttonRed = Button(23)
    # buttonGreen = Button(24)
    # buttonBlue = Button(25)

    # # Main demo loop.
    # try:
    #     print("Started demo!", flush=True)
    #     while True:
    #         if buttonRed.is_pressed:
    #             print("Setting strand to red!", flush=True)
    #             # colorWipe(strip, Color(255, 0, 0))
    #         elif buttonGreen.is_pressed:
    #             print("Setting strand to green!", flush=True)
    #             # colorWipe(strip, Color(0, 255, 0))
    #         elif buttonBlue.is_pressed:
    #             print("Setting strand to blue!", flush=True)
    #             # colorWipe(strip, Color(0, 0, 255))

    # # Always clear LEDs at the end.
    # except KeyboardInterrupt:
    #     colorWipe(strip, Color(0, 0, 0), 10)

if __name__ == '__main__':
    main()
