# N-Body Simulation in Python
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

## Technologies Used:
**Python:** 3.10.12 

**matplotlib:** for visualization 

**multiprocessing:** for parallel computations 

**tkinter:** for simple GUI alerts 

**CSV:** for data export and comparison 

## Version:  
**Python**: 3.10.12

## Overview:  
This project simulates the gravitational interaction between celestial bodies (e.g. **Sun**, **Earth**, **Mars** and **Venus**). The simulation is performed both sequentially and in parallel using Python’s multiprocessing. The results are visualized using matplotlib animation, and stored in CSV files for further analysis. 

## Project Structure:
**main.py**(starting point of your program), 
**.gitignore**(ignore csv when pushing to git), 
**nbody_seq** and **nbody_par** as csv outputs after starting program..

## Main Concepts:
**Newton's Law of Universal Gravitation** is used to calculate forces.
**Euler Integraton** is used to update positions and velocities.
**Supports paralel processing** for force computation using **multiprocessing.Pool**.
**Uses CSV output for data inspection and comparison**.
**Animates** the simulation using **matplotlib's FuncAnimation**.
**Uses tkinter dialogs** to show ersult status after animation ends.

## Code structure:

### Body class:
**name** as string identifier (Sun, Earth..)
**mass** in kilograms,
**x,y** - positions in meters,
**vx, vy** - velocity components in m/s,
**method** - converts body state to a CSV row.

### compute_force()
**Info: Computes the net gravitational force on one body from all others.**
**Input: A tuple of one body and list of all bodies.**
**Output: Net force (fx,fy).**

### update_bodies()
**Info: Updates all body states for one timestep.**
**dt: Time step in seconds.**
**parallel: If true, use multiprocessing, else use single processing**

### simulate()
**Info: Runs the entire simulation for n_iterations.**
**Input: Number of iterations, dt and is parrallel**
**Output: Returning a list of body states at each iteration.**

### write_to_csv()
**data: List of lists of Body(celestial) objects over time...**

### results_are_compatible()
**Info: Compare two simulations for numerical similarity - Checking if positions and velocities are withing a margin of error..**

### plot_simulation()
**Info: Animates the simulation using matplotlib. Displays a live plot and shows tkinter dialog after animation ended.**

## Main Execution flow:
### 1. Runs sequential simulation,
### 2. Saves results to nbody_seq.csv
### 3. Runs parallel simulation
### 4. Saves results to nbody_par.csv
### 5. Compares the results for compatibility
### 6. Displays animation of sequential simulation

## These are Math Formulas I have used in this project
1. Distance Formula (Pythagorean theorem)
   Calculate distance between bodies i and y: r = √((xj - xi)² + (yj - yi)²)
   https://en.wikipedia.org/wiki/Pythagorean_theorem
```
dx = body_j.x - body_i.x
dy = body_j.y - body_i.y
dist = math.hypot(dx, dy)
```

2. Newtons Law of Universal Gravitation
   Gravitation force between two bodies: F = G * (mi * mj) / r²
   https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation

```
force = G * body_i.mass * body_j.mass / dist**2
```

3. Force Components and Acceleration - Newtons Second Law of Motion
   Force is decomposed into x and y, and then acceleration is computed using Newtons second law:
   Fx = F * (dx / r), Fy = F * (dy / r)
   ax = Fx / mi, ay = Fy / mi
   https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion

```
fx += force * dx / dist
fy += force * dy / dist
ax = fx / body.mass
ay = fy / body.mass
```

4. Euler-Cromer Integration (Numerical Method)
   Velocities are updated first using acceleration, and positions are updated using the new velocities:
   vx(t+Δt) = vx(t) + ax * Δt
   x(t+Δt) = x(t) + vx(t+Δt) * Δt
   vy(t+Δt) = vy(t) + ay * Δt
   y(t+Δt) = y(t) + vy(t+Δt) * Δt
   https://en.wikipedia.org/wiki/Euler_method#Semi-implicit_Euler_method

```
body.vx += ax * dt
body.vy += ay * dt
body.x += body.vx * dt
body.y += body.vy * dt
```


## Getting Started:   
Clone this repo, navigate to root folder and start project with **python main.py** or **python3 main.py**. If you don't have **matlibplot** or **tkinter**, then you need to install them with **pip/pip3**... 

**NOTE: IF YOU FACE ANY PROBLEM, PLEASE CONTACT ME :)**

## Author

**Andrej Stjepanović**  
Software Developer
