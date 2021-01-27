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
