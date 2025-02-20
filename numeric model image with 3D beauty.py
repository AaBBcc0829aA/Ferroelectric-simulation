import numpy as np
import pyvista as pv

# Parameters for the triaxial braid
length = 10  # Length of the braid
radius = 1   # Radius of the braid
num_fibers = 3  # Number of fiber sets (e.g., triaxial)
num_turns = 5   # Number of braid turns over the length
points_per_turn = 100  # Resolution of the braid

# Generate triaxial braid paths
angles = np.linspace(0, 2 * np.pi * num_turns, num_turns * points_per_turn)
z = np.linspace(0, length, num_turns * points_per_turn)

# Generate paths for fibers
fibers = []
for i in range(num_fibers):
    phase_shift = i * (2 * np.pi / num_fibers)  # Phase shift for each fiber set
    x = radius * np.cos(angles + phase_shift)
    y = radius * np.sin(angles + phase_shift)
    fibers.append(np.column_stack((x, y, z)))

# Create a pyvista mesh for the fibers
fiber_meshes = []
for fiber in fibers:
    # Create a smooth tube for each fiber
    points = fiber
    line = pv.Spline(points, points_per_turn)
    tube = line.tube(radius=0.1)
    fiber_meshes.append(tube)

# Combine all fiber meshes into one
combined_mesh = fiber_meshes[0]
for tube in fiber_meshes[1:]:
    combined_mesh += tube

# Visualization with improved 3D aesthetics
plotter = pv.Plotter()
plotter.add_mesh(combined_mesh, color="steelblue", smooth_shading=True, specular=0.5, specular_power=20)
plotter.set_background("white")
plotter.show_bounds(grid="front", location="outer", color="black")
plotter.view_isometric()
plotter.show()
