import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

# Load CSV
data = pd.read_csv("simulation_log.csv")

vehicles = sorted(data["VehicleID"].unique())
num_vehicles = len(vehicles)

SAFE_DISTANCE = 10
CAR_LENGTH = 4

fig, ax = plt.subplots(figsize=(12, 4))
ax.set_xlim(0, data["Position"].max() + 20)
ax.set_ylim(-2, 2)
ax.set_title("V2V Vehicle Movement Simulation with Alerts")
ax.set_xlabel("Road Position (meters)")
ax.get_yaxis().set_visible(False)

# Car objects
cars = []
speed_texts = []
alert_texts = []
distance_texts = []
distance_lines = []

for i in range(num_vehicles):
    car = Rectangle((0, -0.3), CAR_LENGTH, 0.6, color="blue")
    ax.add_patch(car)
    cars.append(car)

    speed_text = ax.text(0, 0.7, "", ha="center", fontsize=9)
    speed_texts.append(speed_text)

    alert_text = ax.text(0, 1.1, "", ha="center", fontsize=10, color="red", fontweight="bold")
    alert_texts.append(alert_text)

for i in range(num_vehicles - 1):
    line, = ax.plot([], [], "k--")
    distance_lines.append(line)

    dist_text = ax.text(0, -0.8, "", ha="center", fontsize=8)
    distance_texts.append(dist_text)

def update(frame):
    step_data = data[data["TimeStep"] == frame].sort_values("VehicleID")

    positions = step_data["Position"].values
    speeds = step_data["Speed"].values
    alerts = step_data["Alert"].values

    # Update vehicles
    for i in range(num_vehicles):
        x = positions[i]
        cars[i].set_xy((x, -0.3))
        cars[i].set_color("red" if alerts[i] else "blue")

        speed_texts[i].set_position((x + CAR_LENGTH/2, 0.7))
        speed_texts[i].set_text(f"{speeds[i]} m/s")

        alert_texts[i].set_position((x + CAR_LENGTH/2, 1.1))
        alert_texts[i].set_text("ALERT" if alerts[i] else "")

    # Update distance lines and text
    for i in range(num_vehicles - 1):
        x1 = positions[i] + CAR_LENGTH
        x2 = positions[i+1]
        dist = x2 - x1

        distance_lines[i].set_data([x1, x2], [0, 0])
        distance_texts[i].set_position(((x1 + x2) / 2, -0.8))
        distance_texts[i].set_text(f"{dist:.1f} m")

    return cars + speed_texts + alert_texts + distance_lines + distance_texts

ani = FuncAnimation(fig, update, frames=data["TimeStep"].nunique(), interval=500)
plt.show()
