import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
data = pd.read_csv("simulation_log.csv")

# Plot vehicle positions over time
plt.figure()
for vid in data["VehicleID"].unique():
    vehicle_data = data[data["VehicleID"] == vid]
    plt.plot(vehicle_data["TimeStep"], vehicle_data["Position"], label=f"Vehicle {vid}")

plt.xlabel("Time Step")
plt.ylabel("Position")
plt.title("Vehicle Position Over Time (V2V Simulation)")
plt.legend()
plt.show()
