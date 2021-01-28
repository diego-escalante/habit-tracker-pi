#!/bin/bash

cd "$(dirname "$0")"

if [ "$PWD" != "/opt/habit-tracker-pi" ]; then
    echo "habit-tracker-pi is not located under /opt, please move the tracker there."
    exit 1
fi

echo "Setting up Habit Tracker Pi!"

# Updating, Upgrading
echo "Updating and Upgrading."
sudo apt-get update && sudo apt-get upgrade

# Updater Daemon
echo "Setting up Updater Daemon"
sudo systemctl disable habit-tracker-updater.service
sudo systemctl stop habit-tracker-updater.service
sudo cp daemons/habit-tracker-updater.service /etc/systemd/system/
sudo systemctl enable habit-tracker-updater.service
sudo systemctl start habit-tracker-updater.service

# Habit Tracker Daemon
echo "Setting up Habit Tracker Daemon"
sudo systemctl disable habit-tracker.service
sudo systemctl stop habit-tracker.service
sudo cp daemons/habit-tracker.service /etc/systemd/system/
sudo systemctl enable habit-tracker.service
sudo systemctl start habit-tracker.service

# Clean up excess logs every day
echo "Setting up log cleanup cron"
crontab -l | { sed '/journalctl --vacuum-size=128M/d'; echo "0 0 * * * journalctl --vacuum-size=128M"; } | crontab -

# Install ws281x library
echo "Installing ws281x library"
sudo pip3 install rpi_ws281x==4.2.4
