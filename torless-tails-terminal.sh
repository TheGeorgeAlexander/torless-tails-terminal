#!/bin/bash



# Function that runs in clearnet and unshare
run_in_clearnet() {

    # Location of the proxy server and bashrc file
    PROXY_SERVER="./socks5_proxy_server.py"
    BASHRC="./bashrc"


    # To make sure multiple terminals won't spawn multiple proxy servers
    LOCK_FILE="/var/run/torless_tails_terminal.lock"

    # Function to start the proxy server if it isn't running
    start_proxy_server() {
        if [ -f "$LOCK_FILE" ]; then
            read PID COUNTER < "$LOCK_FILE"
            if kill -0 "$PID" 2>/dev/null; then
                # Increment the process counter in the lock file
                echo "$PID $((COUNTER + 1))" > "$LOCK_FILE"
            else
                # If the proxy server isn't running, start a new one
                start_new_proxy_server
            fi
        else
            # If the lock file doesn't exist, start a new proxy server
            start_new_proxy_server
        fi
    }


    # Function to start a new proxy server and initialize the lock file
    start_new_proxy_server() {
        python3 "$PROXY_SERVER" &
        PID=$!
        echo "$PID 1" > "$LOCK_FILE"
    }


    # Function to edit the lock file on exit
    cleanup() {
        if [ -f "$LOCK_FILE" ]; then
            read PID COUNTER < "$LOCK_FILE"
            # Decrement the counter, kill proxy server if this was last terminal open
            if [ "$COUNTER" -le 1 ]; then
                kill "$PID"
                rm -f "$LOCK_FILE"
            else
                echo "$PID $((COUNTER - 1))" > "$LOCK_FILE"
            fi
        fi
    }


    # Mount the /etc/resolv.conf with the clearnet version to fix DNS queries
    mount --bind /etc/resolv-over-clearnet.conf /etc/resolv.conf

    # Set up a trap to clean up on Bash shell exit
    trap 'cleanup' EXIT

    # Attempt to start the proxy server
    start_proxy_server

    # Run as user, open Bash with the custom init file
    /usr/local/lib/run-with-user-env bash --init-file $BASHRC
}

# Go to clearnet network namespace and unshare mount, then run the function
sudo ip netns exec clearnet unshare --mount -- bash -c "$(declare -f run_in_clearnet); run_in_clearnet"
