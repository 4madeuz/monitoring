#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <command> <output_file> [--restart] [--timeout <seconds>]"
    exit 1
fi

command="$1"
output_file="$2"

restart_on_failure=false
timeout=

for arg in "$@"; do
    case "$arg" in
        --restart)
            restart_on_failure=true
            ;;
        --timeout)
            timeout="$2"
            shift
            ;;
    esac
    shift
done

monitor_process() {
    while true; do
        start_time=$(date +%s)
        $command >> "$output_file" 2>&1 &
        pid=$!
        wait "$pid"
        
        if $restart_on_failure; then
            sleep 1  # Delay before restarting
        else
            break
        fi
    done
}

if [ -n "$timeout" ]; then
    ( sleep "$timeout"; kill -TERM $$ ) &
    timeout_pid=$!
fi

trap 'trap - TERM && kill -- -$$' INT TERM EXIT

monitor_process

if [ -n "$timeout_pid" ]; then
    kill "$timeout_pid" > /dev/null 2>&1
fi
