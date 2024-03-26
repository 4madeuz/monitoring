import subprocess
import time
import os
import signal
import sys

def monitor_process(command, output_file, restart_on_failure=False, timeout=None):
    while True:
        start_time = time.time()
        with open(output_file, 'a') as f:
            try:
                process = subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT)
                while True:
                    if process.poll() is not None:
                        break
                    if timeout is not None and time.time() - start_time > timeout:
                        os.kill(process.pid, signal.SIGTERM)
                        f.write(f"Process timed out after {timeout} seconds and was terminated.\n")
                        break
                    time.sleep(1)
            except Exception as e:
                f.write(f"Error occurred: {str(e)}\n")

        if restart_on_failure:
            time.sleep(1)  # Delay before restarting
        else:
            break

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python monitor_process.py <command> <output_file> [--restart] [--timeout <seconds>]")
        sys.exit(1)

    command = sys.argv[1:]
    output_file = command.pop(1)

    restart_on_failure = "--restart" in sys.argv
    timeout_index = sys.argv.index("--timeout") if "--timeout" in sys.argv else None
    timeout = int(sys.argv[timeout_index + 1]) if timeout_index is not None else None

    monitor_process(command, output_file, restart_on_failure, timeout)
