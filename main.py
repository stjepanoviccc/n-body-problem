import csv
import math
from multiprocessing import Pool
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox

G = 6.67430e-11
N_INTERATIONS = 500 # for more circular orbits, use 1500+ (little more loading of animation)
SEQ_FILE = "outputs/nbody_seq.csv"
PAR_FILE = "outputs/nbody_par.csv"

# Celestial object - name, mass(kg), position(x,y), velocity(vx,vy)
class Body:
    def __init__(self, name, mass, x, y, vx, vy):
        self.name = name
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def to_row(self):
        return [self.name, self.x, self.y, self.vx, self.vy]

# Compute gravitational force on a body from all others - Send a tuple of body/bodies and output is net force(fx,fy)
def compute_force(args):
    body_i, bodies = args
    fx, fy = 0.0, 0.0
    for body_j in bodies:
        if body_i == body_j:
            continue
        dx = body_j.x - body_i.x
        dy = body_j.y - body_i.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue
        force = G * body_i.mass * body_j.mass / dist**2
        fx += force * dx / dist
        fy += force * dy / dist
    return (fx, fy)

# Updates all body states for one timestep (dt in seconds)
# If parallel is True, uses multiprocessing to compute forces in parallel
def update_bodies(bodies, dt, parallel=False):
    if parallel:
        with Pool() as pool:
            forces = pool.map(compute_force, [(b, bodies) for b in bodies])
    else:
        forces = [compute_force((b, bodies)) for b in bodies]

    for i, body in enumerate(bodies):
        fx, fy = forces[i]
        ax = fx / body.mass
        ay = fy / body.mass
        body.vx += ax * dt
        body.vy += ay * dt
        body.x += body.vx * dt
        body.y += body.vy * dt

# filename(where to write), data(list of Body objects for each iteration)
def write_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["iteration", "name", "x", "y", "vx", "vy"])
        for i, bodies in enumerate(data):
            for body in bodies:
                writer.writerow([i] + body.to_row())

# Runs the entire simulation for n_iterations with a given timestep dt
# If parallel is True, uses multiprocessing to update bodies in parallel
def simulate(n_iterations=100, dt=60, parallel=False):
    earth_x = 1.496e11
    earth_y = 0
    earth_vx = 0
    earth_vy = 29780

    mars_x = 2.279e11
    mars_y = 0
    mars_vx = 0
    mars_vy = 24077

    venus_x = 1.082e11
    venus_y = 0
    venus_vx = 0
    venus_vy = 35020

    bodies = [
        Body("Sun", 1.989e30, 0, 0, 0, 0),
        Body("Earth", 5.972e24, earth_x, earth_y, earth_vx, earth_vy),
        Body("Mars", 6.417e23, mars_x, mars_y, mars_vx, mars_vy),
        Body("Venus", 4.867e24, venus_x, venus_y, venus_vx, venus_vy),
    ]

    results = []
    for _ in range(n_iterations):
        update_bodies(bodies, dt, parallel=parallel)
        results.append([Body(b.name, b.mass, b.x, b.y, b.vx, b.vy) for b in bodies])
    return results

# Animates the simulation results using matplotlib
def plot_simulation(data, compatibility=None):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    limit = 2.5e11
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    names = [b.name for b in data[0]]
    colors = {'Sun': 'yellow', 'Earth': 'blue', 'Mars': 'red', 'Venus': 'orange'}
    sizes = {'Sun': 80, 'Earth': 20, 'Mars': 15, 'Venus': 18}

    scatters = [ax.plot([], [], 'o', color=colors.get(name, 'black'), label=name, ms=sizes.get(name, 6))[0] for name in names]

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Sun', markerfacecolor='yellow', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Earth', markerfacecolor='blue', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Mars', markerfacecolor='red', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Venus', markerfacecolor='orange', markersize=10),
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    def update(frame):
        bodies = data[frame]
        for scatter, body in zip(scatters, bodies):
            scatter.set_data([body.x], [body.y])
        ax.set_title(f"Iteration: {frame}")

        if frame == len(data) - 1:
            ani.event_source.stop()
            root = tk.Tk()
            root.withdraw()
            if compatibility is None:
                msg = "Simulation ended."
            elif compatibility:
                msg = "Simulations are compatible."
            else:
                msg = "Simulacije are not compatible!"
            messagebox.showinfo("End of simulation.", msg)
            root.destroy()

        return scatters

    ani = FuncAnimation(fig, update, frames=len(data), interval=50, blit=True)
    plt.show()

# Compares two sets of simulation results for compatibility
# Returns True if results are compatible within a given epsilon tolerance
def results_are_compatible(data1, data2, epsilon=1e5):
    if len(data1) != len(data2):
        return False
    for bodies1, bodies2 in zip(data1, data2):
        if len(bodies1) != len(bodies2):
            return False
        for b1, b2 in zip(bodies1, bodies2):
            dx = abs(b1.x - b2.x)
            dy = abs(b1.y - b2.y)
            dvx = abs(b1.vx - b2.vx)
            dvy = abs(b1.vy - b2.vy)
            if dx > epsilon or dy > epsilon or dvx > epsilon or dvy > epsilon:
                return False
    return True

if __name__ == '__main__':
    dt = 60 * 60 * 6

    print("Starting sequential simulation...")
    data_seq = simulate(n_iterations=N_INTERATIONS, dt=dt, parallel=False)
    write_to_csv(SEQ_FILE, data_seq)

    print("Starting parallel simuation...")
    data_par = simulate(n_iterations=N_INTERATIONS, dt=dt, parallel=True)
    write_to_csv(PAR_FILE, data_par)

    print("Compare simulation results...")
    compatible = results_are_compatible(data_seq, data_par)

    print("Showing sequential simulation...")
    plot_simulation(data_seq, compatibility=compatible)
