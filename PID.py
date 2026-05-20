import psutil   # Allows us to interact with system processes
import time     # Gives us access to sleep() for delays


# Print a startup message so we know the monitor is running
print("=== Process Monitor Started ===")


# Create an empty set
# A set stores unique values
# We will use it to remember processes we already know about
known_processes = set()


# Loop through ALL currently running processes
# process_iter() gives us one process at a time
#
# ['pid', 'name']
# means:
# "only collect the PID and process name"
#
# This is faster than collecting ALL information
for process in psutil.process_iter(['pid', 'name']):

    try:
        # Create a tuple:
        # (PID, Process Name)
        #
        # Example:
        # (1234, "firefox")
        proc_info = (
            process.info['pid'],
            process.info['name']
        )

        # Add the process tuple into our set
        known_processes.add(proc_info)

    # Sometimes a process closes while we're reading it
    # or we don't have permission to access it
    #
    # Instead of crashing the program,
    # we simply ignore those processes
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass


# Infinite loop
# The monitor will keep running forever
while True:

    # Create a NEW empty set
    # This will store the processes from THIS scan
    current_processes = set()


    # Loop through all running processes AGAIN
    for process in psutil.process_iter(['pid', 'name']):

        try:
            # Again create:
            # (PID, Process Name)
            proc_info = (
                process.info['pid'],
                process.info['name']
            )

            # Add current process to current_processes set
            current_processes.add(proc_info)

        # Ignore inaccessible/disappearing processes
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


    # Compare sets
    #
    # current_processes - known_processes
    #
    # Meaning:
    # "Show processes that exist NOW
    # but did NOT exist BEFORE"
    #
    # These are NEW processes
    new_processes = current_processes - known_processes


    # Loop through every newly detected process
    for pid, name in new_processes:

        # Print information about the new process
        print(f"[NEW] Process started: {name} (PID: {pid})")


    # Compare sets again
    #
    # known_processes - current_processes
    #
    # Meaning:
    # "Show processes that existed BEFORE
    # but do NOT exist NOW"
    #
    # These are CLOSED processes
    closed_processes = known_processes - current_processes


    # Loop through every closed process
    for pid, name in closed_processes:

        # Print information about the closed process
        print(f"[CLOSED] Process ended: {name} (PID: {pid})")


    # IMPORTANT:
    # Update the old process list
    #
    # So next scan becomes:
    # "compare against current scan"
    known_processes = current_processes


    # Wait 1 second before scanning again
    #
    # Without this:
    # the loop would run insanely fast
    # and use huge CPU
    time.sleep(1)

    #I hope this helped you to understand psutil better. :) // Pozdravi Joropentagrama
