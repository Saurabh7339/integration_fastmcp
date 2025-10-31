#!/bin/bash

# Exit on any error
set -e


# Function to kill processes on port 8012
kill_port_processes() {
    echo "Killing processes on port 8000..."
    if fuser 8000/tcp > /dev/null 2>&1; then
        fuser -k 8000/tcp
        echo "Processes on port 8000 terminated."
    else
        echo "No processes found on port 8000."
    fi
}

kill_port_processes2() {
    echo "Killing processes on port 8030..."
    if fuser 8030/tcp > /dev/null 2>&1; then
        fuser -k 8030/tcp
        echo "Processes on port 8030 terminated."
    else
        echo "No processes found on port 8030."
    fi
}
kill_port_processes3() {
    echo "Killing processes on port 8031..."
    if fuser 8031/tcp > /dev/null 2>&1; then
        fuser -k 8031/tcp
        echo "Processes on port 8031 terminated."
    else
        echo "No processes found on port 8031."
    fi
}

kill_port_processes4() {
    echo "Killing processes on port 8032..."
    if fuser 8032/tcp > /dev/null 2>&1; then
        fuser -k 8032/tcp
        echo "Processes on port 8032 terminated."
    else
        echo "No processes found on port 8032."
    fi
}


    # Execute the functions
kill_port_processes
kill_port_processes2
kill_port_processes3
kill_port_processes4
echo "Script execution completed."