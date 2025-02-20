
import numpy as np
import pyvista as pv

# Parameters for the triaxial braid
length = 10  # Length of the braid
radius = 1   # Radius of the braid
num_fibers = 6  # Number of interwoven fibers
num_turns = 5   # Number of braid turns over the length
points_per_turn = 100  # Resolution of the braid

# Generate the z-axis (length direction) and angles for the braiding
z = np.linspace(0, length, num_turns * points_per_turn)
angles = np.linspace(0, 2 * np.pi * num_turns, num_turns * points_per_turn)

# Generate braided paths
fibers = []
for i in range(num_fibers):
    # Phase shift for interwoven fibers
    phase_shift = (i * 2 * np.pi) / num_fibers
    if i % 2 == 0:  # Fibers going in one direction
        x = radius * np.cos(angles + phase_shift)
        y = radius * np.sin(angles + phase_shift)
    else:  # Fibers going in the opposite direction (crossing)
        x = radius * np.cos(-angles + phase_shift)
        y = radius * np.sin(-angles + phase_shift)
    fibers.append(np.column_stack((x, y, z)))

# Create a pyvista mesh for the fibers
combined_mesh = pv.PolyData()
for fiber in fibers:
    # Create individual fibers with spline interpolation
    points = fiber
    line = pv.Spline(points, points_per_turn)
    tube = line.tube(radius=0.05)  # Create tubes to represent fibers
    combined_mesh = combined_mesh.merge(tube)  # Merge each fiber into a single mesh

# Visualization with improved 3D aesthetics
plotter = pv.Plotter()
plotter.add_mesh(combined_mesh, color="steelblue", smooth_shading=True, specular=0.5, specular_power=20)
plotter.set_background("white")
plotter.show_bounds(grid="front", location="outer", color="black")
plotter.view_isometric()
plotter.show()
