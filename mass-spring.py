import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# System parameters
m = 1.0      # mass (kg)
k = 10.0     # spring constant (N/m)
x0 = 1.0     # initial displacement from equilibrium (m)
v0 = 0.0     # initial velocity (m/s)
g = 9.81     # gravity (m/s^2)

# Static equilibrium position (where spring force balances gravity)
y_eq = m * g / k

# Derived parameters
omega = np.sqrt(k/m)
t = np.linspace(0, 10, 500)
# Motion about equilibrium
y = y_eq + x0 * np.cos(omega * t) + (v0/omega) * np.sin(omega * t)

# Animation setup
fig, ax = plt.subplots(figsize=(3, 6))
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.1, 1.2)
ax.set_xticks([])
ax.set_title("Hanging Mass-Spring System Animation")

# Draw fixed top
ax.plot([0, 0], [1.1, 1.2], color='black', lw=4)

# Initialize spring and mass
spring_line, = ax.plot([], [], 'b-', lw=2)
mass_patch = plt.Rectangle((-0.15, y[0]-0.1), 0.3, 0.15, fc='red')
ax.add_patch(mass_patch)

def animate(i):
    # Spring coordinates (vertical, hanging from y=1.2 to y[i])
    spring_y = np.linspace(1.2, y[i], 100)
    spring_x = 0.05 * np.sin(10 * np.pi * (spring_y - y[i]) / (1.2 - y[i]))
    spring_line.set_data(spring_x, spring_y)
    # Move mass
    mass_patch.set_xy((-0.15, y[i]-0.1))
    return spring_line, mass_patch

ani = FuncAnimation(fig, animate, frames=len(t), interval=20, blit=True)
plt.show()