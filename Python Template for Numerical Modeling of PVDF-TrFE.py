import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Material Properties
youngs_modulus = 843e6  # Pa (Elastic modulus)
poisson_ratio = 0.35    # Typical for PVDF
piezoelectric_coeff = 33e-12  # C/N (d33 for PVDF-TrFE)
density = 1.78e3  # kg/m^3 (Density for PVDF-TrFE)

# Geometric Parameters
length = 0.02  # Length of the sample in meters
area = 1.0e-6  # Cross-sectional area in m^2
thickness = 200e-6  # Thickness of PVDF film in meters

 # Simulation Parameters
applied_force = np.linspace(0, 50, 100)  # Force range in N
strain = applied_force / (youngs_modulus * area)
stress = applied_force / area

# Voltage Generation (d33 Mode)
voltage_generated = piezoelectric_coeff * stress * thickness

# Dynamic Simulation of Voltage Response
def piezo_response(y, t, k, m, d):
    displacement, velocity = y
    force = 10 * np.sin(2 * np.pi * 1 * t)  # 1 Hz sinusoidal force
    dydt = [velocity, (force - d * velocity - k * displacement) / m]
    return dydt

# Parameters for dynamic simulation
mass = density * area * length
spring_constant = youngs_modulus * area / length
damping = 0.05 * spring_constant  # 5% damping

# Initial conditions and time array
y0 = [0, 0]  # Initial displacement and velocity
time = np.linspace(0, 5, 500)  # 5 seconds, 500 points

# Solve ODE for displacement
response = odeint(piezo_response, y0, time, args=(spring_constant, mass, damping))
displacement = response[:, 0]

# Voltage induced by dynamic excitation
dynamic_stress = spring_constant * displacement / area
dynamic_voltage = piezoelectric_coeff * dynamic_stress * thickness

# Plot Stress-Strain Curve
plt.figure(figsize=(8, 5))
plt.plot(strain, stress, label="Stress-Strain Curve", color='b')
plt.xlabel("Strain")
plt.ylabel("Stress (Pa)")
plt.title("Stress-Strain Behavior of PVDF")
plt.legend()
plt.grid()

# Plot Voltage vs Force
plt.figure(figsize=(8, 5))
plt.plot(applied_force, voltage_generated * 1e3, label="Voltage Generation", color='r')
plt.xlabel("Applied Force (N)")
plt.ylabel("Generated Voltage (mV)")
plt.title("Piezoelectric Voltage vs Force")
plt.legend()
plt.grid()

# Plot Dynamic Voltage Response
plt.figure(figsize=(8, 5))
plt.plot(time, dynamic_voltage * 1e3, label="Dynamic Voltage Response", color='g')
plt.xlabel("Time (s)")
plt.ylabel("Voltage (mV)")
plt.title("Dynamic Voltage Response")
plt.legend()
plt.grid()
plt.show()
