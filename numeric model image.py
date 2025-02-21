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
mesh = pv.PolyData()

for fiber in fibers:
    points = fiber
    mesh = mesh.merge(pv.PolyData(points))

# Add triangular faces to mimic a braided structure
for i in range(len(fibers[0]) - 1):
    for j in range(num_fibers):
        next_fiber = (j + 1) % num_fibers
        mesh.faces = np.hstack([
            [3, i, i + 1, next_fiber + 1]
        ])

# Visualization
plotter = pv.Plotter()
plotter.add_mesh(mesh, color="lightgray", show_edges=True, opacity=0.7)
plotter.show()
