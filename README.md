# Habit Tracker Pi

<p align="center">
  <picture>
    <source srcset="../assets/tracker.png?raw=true">
    <img alt="Shows a picture of the habit tracker." src="../assets/traker.png?raw=true">
  </picture>
</p>

A Habit Tracker that runs on a Raspberry Pi. It is a Python program that controls a strip of LEDs connected to the Pi in the configuration of a 6x7 grid to display a calendar month.

## Features
* Automatically boots up the python program when the Pi is turned on.
* Automatically display the current month and day.
* Button input allows the user to change the color status of the currently selected day (RED, GREEN, CYAN).
* Button inputs allow the user to scroll through past days, allowing the user to see historical data months and years in the past.
* Day states are automatically saved. In case the Pi loses power, no data is lost and the Pi will automatically load it all back in next time it is turned on.
* Turns off LEDs during sleep hours to save power and not emit light. The user can tap on a button to temporarily turn on the display.
* Automatically pulls updates from the internet and restarts the tracker.

## Setup
1. From your Raspberry Pi, clone this repo.
2. Put the repo under `/opt`.
3. Run `/opt/habit-tracker-pi/setup.sh`.

## Troubleshooting
<details>
  <summary>I get a ws2811_init failed runtime error when trying to run the tracker manually.</summary>
  
  You need to run it with root privileges if you are running it manually. 
</details>

## Notes
This is a repo for a very specific, physical, and personal project. Updates to the repo automatically affect the build. Therefore, feel free to look around, but it is unlikely that any changes by others will be accepted into this repo.
