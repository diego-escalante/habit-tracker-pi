#!/bin/bash

cd "$(dirname "$0")"

while true; do
    sleep 5
    echo "Checking for Habit Tracker updates..."

    BRANCH=$(git rev-parse --abbrev-ref HEAD)

    echo "Using current branch: $BRANCH"
    git fetch

    if ! git ls-remote --heads origin ${BRANCH} | grep ${BRANCH} > /dev/null; then
        echo "Branch does not exist in remote. Ignoring!"
        continue
    fi

    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    BASE=$(git merge-base @ @{u})

    if [ $LOCAL = $REMOTE ]; then
        echo "Habit Tracker is up to date."
    elif [ $LOCAL = $BASE ]; then
        echo "Found update. Stopping Habit Tracker in order to perform upgrade."
        sudo systemctl stop habit-tracker.service
        echo "Pulling latest changes!"
        git merge FETCH_HEAD
        echo "Habit Tracker has been updated! Restarting Habit Tracker."
        sudo systemctl start habit-tracker.service
	echo "Restarting Updater."
        exit
    elif [ $REMOTE = $BASE ]; then
        echo "Local is ahead of remote. Ignoring! Push to re-enable updater."
    else
        echo "Local and remote diverged. Ignoring! Rebase or merge to re-enable updater."
    fi
done
