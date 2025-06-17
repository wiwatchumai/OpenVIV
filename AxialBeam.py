import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Variables definittion for a beam in two-dimensional space: x-t (displacement-time)
t=sp.symbols('t')
x=sp.symbols('x')
# Define the displacement function of a beam
u=sp.Function('u')
E, rho, A, l = sp.symbols('E rho A l')  # Young's modulus, density, cross-sectional area, length
# Define the wave equation for a beam
PDE = sp.Eq(rho*u(x, t).diff(t, 2) - E*A*u(x, t).diff(x, 2), 0)

E=float(input("Enter the Young's modulus (E [Pascarl]): "))
rho=float(input("Enter the density (rho [kg/m^3]): "))
l=float(input("Enter the length of the beam (l [m]): "))

# Identify the beam's cross-sectional area shape

print(" Five common cross-sectional shapes includes " \
"\n 1. Rectangular (R) " \
"\n 2. Circular (CI)" \
"\n 3. Hollow-Circular (HC)" \
"\n 4. I" \
"\n 5. T" \
"\n 6. C " \
"\n 7. Square")210
cross_section_shape = input("Enter the cross-sectional shape: ")
if cross_section_shape == 'R':
    width = float(input("Enter the width of the rectangular cross-section (m): "))
    height = float(input("Enter the height of the rectangular cross-section (m): "))
    A = width * height  # Area of rectangular cross-section
elif cross_section_shape == 'CI':
    radius = float(input("Enter the radius of the circular cross-section (m): "))
    A = np.pi * radius**2
elif cross_section_shape == 'HC':
    outer_radius = float(input("Enter the outer radius of the hollow circular cross-section (m): "))
    inner_radius = float(input("Enter the inner radius of the hollow circular cross-section (m): "))
    A = np.pi * (outer_radius**2 - inner_radius**2)
elif cross_section_shape == 'I':
    width = float(input("Enter the width of the I-beam (m): "))
    height = float(input("Enter the height of the I-beam (m): "))
    flange_thickness = float(input("Enter the thickness of the flanges (m): "))
    web_thickness = float(input("Enter the thickness of the web (m): "))
    A = (width * flange_thickness * 2) + (height - 2 * flange_thickness) * web_thickness
elif cross_section_shape == 'T':
    width = float(input("Enter the width of the T-beam (m): "))
    height = float(input("Enter the height of the T-beam (m): "))
    flange_thickness = float(input("Enter the thickness of the flange (m): "))
    web_thickness = float(input("Enter the thickness of the web (m): "))
    A = (width * flange_thickness) + ((height - flange_thickness) * web_thickness)
elif cross_section_shape == 'C':
    width = float(input("Enter the width of the C-beam (m): "))
    height = float(input("Enter the height of the C-beam (m): "))
    flange_thickness = float(input("Enter the thickness of the flanges (m): "))
    web_thickness = float(input("Enter the thickness of the web (m): "))
    A = (width * flange_thickness * 2) + (height - 2 * flange_thickness) * web_thickness
elif cross_section_shape == 'S':
    side_length = float(input("Enter the side length of the square cross-section (m): "))
    A = side_length**2  # Area of square cross-section
else:
    print("Invalid cross-sectional shape selected.")
    A = 0


k = E * A / l  # Structural rigidity

# Define the BCs
BC1 = sp.Eq(u(0, t), 0)  # Boundary condition at x=0
BC2 = sp.Eq(u(l, t).diff(x, 1), 0)  # Boundary condition at x=l
BC3 = sp.Eq(u(x, 0).diff(t, 1), 0)  # Boundary condition at t=0

# Input the number of nodes: i
i = int(input("Select the number of nodes : "))

forces = []
for n in range(i):
    if n == i - 1:
        F_n = float(input(f"Input force magnitude at node {n+1}: "))
    else:
        F_n = 0.0
    forces.append(F_n)

for n in range(1, i+1):
    u_n = sp.symbols(f'u{n}')
    u_np1 = sp.symbols(f'u{n+1}')
    F_n = k * (u_n - u_np1)
    print(f"F({n}) =")
    sp.pprint(F_n)

# Assemble global stiffness matrix
K = np.zeros((i, i))
for n in range(i - 1):
    K[n, n]     += k
    K[n, n+1]   -= k
    K[n+1, n]   -= k
    K[n+1, n+1] += k

# Convert forces list to numpy array
F = np.array(forces)

# Apply boundary condition: u0 = 0 (fixed at node 0)
K[0, :] = 0
K[0, 0] = 1
F[0] = 0

# Solve for displacements
u = np.linalg.solve(K, F)

print("Nodal displacements (u_n):")
for n in range(i):
    print(f"u{n} = {u[n]} m.")

# Plot displacement vs node number
plt.figure()
plt.plot(range(i), u, marker='o')
plt.title("Nodal Displacement vs Node Number")
plt.xlabel("Node Number")
plt.ylabel("Displacement (m)")
plt.grid(True)
plt.show()