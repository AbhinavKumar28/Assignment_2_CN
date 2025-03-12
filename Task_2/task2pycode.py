import matplotlib.pyplot as plt

# Load connection start times
start_times = {}
with open("Task_2\connection_start_with_mitigation.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        start_time = float(parts[0])
        conn_id = (parts[1], parts[2], parts[3], parts[4])  # (Src IP, Dst IP, Src Port, Dst Port)
        start_times[conn_id] = start_time

# Load connection end times
durations = []
times = []
with open("Task_2\connection_end_with_mitigation.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        end_time = float(parts[0])
        conn_id = (parts[1], parts[2], parts[3], parts[4])

        if conn_id in start_times:
            duration = end_time - start_times[conn_id]
        else:
            duration = 100  # Default if no end found

        times.append(start_times[conn_id])
        durations.append(duration)

# Plot results
plt.figure(figsize=(10, 5))
plt.scatter(times, durations, color='blue', label='TCP Connection Duration')
plt.axvline(x=20, color='red', linestyle='--', label='Attack Start (20s)')
plt.axvline(x=120, color='green', linestyle='--', label='Attack End (120s)')
plt.xlabel("Connection Start Time (s)")
plt.ylabel("Connection Duration (s)")
plt.title("TCP Connection Duration vs. Start Time")
plt.legend()
plt.grid()
plt.show()
