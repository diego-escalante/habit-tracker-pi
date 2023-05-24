# Habit Tracker Pi
A Habit Tracker that runs on a Raspberry Pi. It is a Python program that controls a strip of LEDs connected to the Pi in the configuration of a calendar-month, which light up in various colors to keep track of the current month, day, and display a history of successes and failures of previous days. Three physical buttons can be pressed to control, view, and change the color-status of any day in the past. It saves the state every time a change is made, so if it loses and regains power, it will automatically start up again and load up the past history.

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
