#!/usr/bin/env python3

# Imports
import time
import rpi_ws281x
import argparse
from gpiozero import Button
import calendar
import datetime
import json
from enum import Enum
from enums import Color, Status

# LED strip configuration.
LED_COUNT = 42        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 1    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Other Constants
BUTTON_LEFT_GPIO_PIN = 23
BUTTON_MIDDLE_GPIO_PIN = 24
BUTTON_RIGHT_GPIO_PIN = 25
HABIT_DATA_FILE = "habit-data.json"

# LED array representing the colors of the display.
leds = [Color.BLANK] * LED_COUNT

# Initialize the Strip of LEDS.
strip = rpi_ws281x.PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Currently selected day.
selectedDay = datetime.datetime.now()

# Habit tracker data in JSON format.
habitData = None

lastInputTime = datetime.datetime.now()

# Clears LEDs colors.
def clearLeds():
    global leds
    leds = [Color.BLANK] * LED_COUNT

def isSleepTime():
    beginTime = datetime.time(hour=23)
    endTime = datetime.time(hour=6)
    currentTime = datetime.datetime.now().time()

    if beginTime < endTime:
        return currentTime >= beginTime and currentTime <= endTime
    else: # crosses midnight
        return currentTime >= beginTime or currentTime <= endTime

def setStripBrightness():
    if (isSleepTime() and lastInputTime + datetime.timedelta(seconds=30) < datetime.datetime.now()):
        strip.setBrightness(0)
    else:
        strip.setBrightness(1)

def displayLed(i):
    setStripBrightness()
    strip.setPixelColor(i, leds[i].value)
    strip.show()

# Display the led colors on the strip.
def displayLeds():
    setStripBrightness()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, leds[i].value)
    strip.show()

def wipeDisplayLeds(intervalMs=25):
    setStripBrightness()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, leds[i].value)
        strip.show()
        time.sleep(intervalMs/1000)

def setMonth():
    clearLeds()
    offset = getOffsetOfMonth(selectedDay.year, selectedDay.month)
    days = getDaysOfMonth(selectedDay.year, selectedDay.month)
    for i in range(offset, days + offset):
        leds[i] = getColorForDay(selectedDay.year, selectedDay.month, i + 1 - offset)

def getColorForDay(year, month, day):
    year = str(year)
    month = str(month)
    day = str(day)
    if year in habitData and month in habitData[year] and day in habitData[year][month]:
        status = habitData[year][month][day]
        if status == Status.GOOD.value:
            return Color.GREEN
        elif status == Status.BAD.value:
            return Color.RED
        elif status == Status.NEUTRAL.value:
            return Color.CYAN
        else:
            print("WARNING! Unknown habit status for " + year + "-" + month + "-" + day, flush=True)
            return Color.YELLOW

    relativeTime = isPastPresentOrFuture(datetime.datetime(year=int(year), month=int(month), day=int(day)))
    if relativeTime == -1:
        return Color.CYAN
    elif relativeTime == 0:
        writeHabitData(selectedDay.year, selectedDay.month, selectedDay.day, Status.BAD.value)
        return Color.RED
    else:
        return Color.WHITE

def getLedForSelectedDay():
    return getOffsetOfMonth(selectedDay.year, selectedDay.month) + selectedDay.day - 1

# Returns the total number of days in the given month.
def getDaysOfMonth(year, month):
    return calendar.monthrange(year, month)[1]

# Returns the weekday offset of the month. Sunday is 0, Saturday is 6. (i.e. if the month starts on a tuesday, return 2.)
def getOffsetOfMonth(year, month):
    # Python considers Monday as day 0, so shift weekday value up by one, looping back to 0 in the case of Sunday.
    return calendar.monthrange(selectedDay.year, selectedDay.month)[0] + 1 % 7

# Lights up red, green, and blue LEDs in order.
def testDisplay():
    primaries = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.CYAN, Color.MAGENTA, Color.WHITE, Color.BLANK]
    for primary in primaries:
        for i in range(strip.numPixels()):
            leds[i] = primary
        wipeDisplayLeds()

# Sets selectedDay to the current local day.
def setSelectedDayToNow():
    global selectedDay

    year = selectedDay.year
    month = selectedDay.month
    leds[getLedForSelectedDay()] = getColorForDay(selectedDay.year, month, selectedDay.day)

    selectedDay = datetime.datetime.now()
    if month != selectedDay.month or year != selectedDay.year:
        setMonth()
    leds[getLedForSelectedDay()] = Color.BLANK
    displayLeds()

# Shifts selectedDay by the delta number of days.
def shiftSelectedDay(delta):
    global selectedDay

    month = selectedDay.month
    leds[getLedForSelectedDay()] = getColorForDay(selectedDay.year, month, selectedDay.day)

    newDay = selectedDay + datetime.timedelta(days=delta)
    if isPastPresentOrFuture(newDay) == 1:
        leds[getLedForSelectedDay()] = Color.BLANK
        displayLed(getLedForSelectedDay())
        return

    selectedDay = newDay

    if month != selectedDay.month:
        setMonth()
    leds[getLedForSelectedDay()] = Color.BLANK
    displayLeds()

def readHabitData():
    global habitData
    try:
        with open(HABIT_DATA_FILE, mode="r", encoding="utf-8") as file:
            habitData = json.load(file)
    except OSError:
        print("OSError: Unable to open file " + HABIT_DATA_FILE, flush=True)

def writeHabitData(year, month, day, status):
    global habitData
    year = str(year)
    month = str(month)
    day = str(day)

    if year not in habitData:
        habitData[year] = {}
    if month not in habitData[year]:
        habitData[year][month] = {}

    habitData[year][month][day] = status

    try:
        with open(HABIT_DATA_FILE, mode="w", encoding="utf-8") as file:
            json.dump(habitData, file)
    except OSError:
        print("OSError: Unable to open file " + HABIT_DATA_FILE, flush=True)


def leftPressed():
    shiftSelectedDay(-1)
    global timestamp, lastInputTime
    timestamp = datetime.datetime.now()
    lastInputTime = datetime.datetime.now()

def middlePressed():
    color = getColorForDay(selectedDay.year, selectedDay.month, selectedDay.day)
    if color == Color.CYAN:
        color = Color.RED
        writeHabitData(selectedDay.year, selectedDay.month, selectedDay.day, Status.BAD.value)
    elif color == Color.GREEN:
        color = Color.CYAN
        writeHabitData(selectedDay.year, selectedDay.month, selectedDay.day, Status.NEUTRAL.value)
    elif color == Color.RED:
        color = Color.GREEN
        writeHabitData(selectedDay.year, selectedDay.month, selectedDay.day, Status.GOOD.value)
    leds[getLedForSelectedDay()] = color
    displayLed(getLedForSelectedDay())
    global timestamp, lastInputTime
    timestamp = datetime.datetime.now()
    lastInputTime = datetime.datetime.now()

def isPastPresentOrFuture(inputDay):
    currentDay = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    inputDay = inputDay.replace(hour=0, minute=0, second=0, microsecond=0)

    if inputDay < currentDay:
        return -1
    elif inputDay > currentDay:
        return 1
    else:
        return 0

def rightPressed():
    shiftSelectedDay(1)
    global timestamp, lastInputTime
    timestamp = datetime.datetime.now()
    lastInputTime = datetime.datetime.now()

def leftHeld():
    buttonLeft.hold_time = 0.1
    leftPressed()

def middleHeld():
    buttonMiddle.hold_time = 0.1
    middlePressed()

def rightHeld():
    buttonRight.hold_time = 0.1
    rightPressed()

def leftReleased():
    buttonLeft.hold_time = 1

def middleReleased():
    buttonMiddle.hold_time = 1

def rightReleased():
    buttonRight.hold_time = 1

# Sets up the GPIO Buttons.
def setupButtons():
    global buttonLeft, buttonMiddle, buttonRight
    buttonLeft = Button(BUTTON_LEFT_GPIO_PIN)
    buttonMiddle = Button(BUTTON_MIDDLE_GPIO_PIN)
    buttonRight = Button(BUTTON_RIGHT_GPIO_PIN)

    buttonLeft.when_pressed = leftPressed
    buttonMiddle.when_pressed = middlePressed
    buttonRight.when_pressed = rightPressed

    buttonLeft.when_held = leftHeld
    buttonMiddle.when_held = middleHeld
    buttonRight.when_held = rightHeld

    buttonLeft.when_released = leftReleased
    buttonMiddle.when_released = middleReleased
    buttonRight.when_released = rightReleased

    buttonLeft.hold_time = 1
    buttonMiddle.hold_time = 1
    buttonRight.hold_time = 1

    buttonLeft.hold_repeat = True
    buttonMiddle.hold_repeat = True
    buttonRight.hold_repeat = True

def main():
    global timestamp
    timestamp = datetime.datetime.now()
    try:
        # Set up GPIO Buttons.
        setupButtons()
        testDisplay()
        readHabitData()

        setMonth()
        wipeDisplayLeds()

        while True:
            currentTime = datetime.datetime.now()
            if timestamp + datetime.timedelta(milliseconds=250) > currentTime:
                time.sleep(0.1)
                continue
            timestamp = currentTime

            # If it's been a while since last button input and a non-present day is selected, reset to that.
            if isPastPresentOrFuture(selectedDay) != 0 and lastInputTime + datetime.timedelta(seconds=30) < currentTime:
                setSelectedDayToNow()

            i = getLedForSelectedDay()
            if leds[i] == Color.BLANK:
                leds[i] = getColorForDay(selectedDay.year, selectedDay.month, selectedDay.day)
            else:
                leds[i] = Color.BLANK
            displayLed(i)
            time.sleep(500/1000)

    except KeyboardInterrupt:
        clearLeds()
        displayLeds()

if __name__ == '__main__':
    main()
