import psutil   
import time    

print("=== Process Monitor Started ===")

known_processes = set()
for process in psutil.process_iter(['pid', 'name']):

    try:
        
        proc_info = (
            process.info['pid'],
            process.info['name']
        )

        
        known_processes.add(proc_info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass



while True:
    current_processes = set()

    for process in psutil.process_iter(['pid', 'name']):

        try:
            proc_info = (
                process.info['pid'],
                process.info['name']
            )

            current_processes.add(proc_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    new_processes = current_processes - known_processes


   
    for pid, name in new_processes:

        print(f"[NEW] Process started: {name} (PID: {pid})")

    closed_processes = known_processes - current_processes

    for pid, name in closed_processes:

        print(f"[CLOSED] Process ended: {name} (PID: {pid})")

    known_processes = current_processes
    time.sleep(1)
