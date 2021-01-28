#!/usr/bin/env python3

import time
from rpi_ws281x import PixelStrip, Color
import argparse
from gpiozero import Button

# LED strip configuration:
LED_COUNT = 42        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 8    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    # Intialize the library (must be called once before other functions).
    strip.begin()

    # Set up GPIO buttons.
    buttonRed = Button(23)
    buttonGreen = Button(24)
    buttonBlue = Button(25)

    # Main demo loop.
    try:
        print("Started demo!", flush=True)
        colorWipe(strip, Color(255, 0, 0))
        while True:
            if buttonRed.is_pressed:
                print("Setting strand to red!", flush=True)
                colorWipe(strip, Color(255, 0, 0))
            elif buttonGreen.is_pressed:
                print("Setting strand to green!", flush=True)
                colorWipe(strip, Color(0, 255, 0))
            elif buttonBlue.is_pressed:
                print("Setting strand to blue!", flush=True)
                colorWipe(strip, Color(0, 0, 255))

    # Always clear LEDs at the end.
    except KeyboardInterrupt:
        colorWipe(strip, Color(0, 0, 0), 10)
