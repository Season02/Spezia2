#!/bin/bash
GLOBAL_PID="PID"

if [ -r "$GLOBAL_PID" ]; then
    # echo "this $GLOBAL_PID"
    PID=`cat "$GLOBAL_PID"`
    echo "PID: $PID"
    kill s -9 $PID >/dev/null 2>&1
    if [ $? -gt 0 ]; then
        echo "PID file found but no matching process was found. Stop aborted."
        exit 1
    fi
    rm -f "$GLOBAL_PID"
    # echo "$PID"
    echo "Project Stoppd"
    exit 0
else
    echo "Unable to read PID file. Stop aborted."
    exit 1
fi