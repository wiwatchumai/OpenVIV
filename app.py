import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os
import matplotlib
from matplotlib.animation import FuncAnimation

matplotlib.use("Agg")  # Ensure compatibility with Streamlit

st.title("OpenBeam: Axial Load Calculator")

st.write("(Made by Wiwat Chumai, Mechanical Engineering Student) This work employs the idea of finite element analysis (FEA) to solve the axial load problem of a beam. The beam is divided into nodes, and the stiffness matrix is constructed based on the cross-sectional area and material properties. The nodal displacements are then computed based on the applied forces.")

E = st.number_input("Young's Modulus (E) [Pa]", value=200e6)
rho = st.number_input("Density (ρ) [kg/m³]", value=7800.0)
l = st.number_input("Beam Length (l) [m]", value=1.0)
i = st.number_input("Number of Nodes", value=4, min_value=2, step=1)

# Identify the beam's cross-sectional area shape
st.write("Five common cross-sectional shapes include:")
st.write("1. Rectangular Beam (R)")
st.write("2. Circular Beam (CI)")
st.write("3. Hollow-Circular (HC)")
st.write("4. I-Beam (I)")
st.write("5. T-Beam (T)")
st.write("6. C-Beam (C)")
st.write("7. Square Beam (S)")
st.write("Each cross-sectional shape will lead to a different calculation results.")


cross_section_shape = st.selectbox(
    "Select the cross-sectional shape:",
    ("Rectangular Beam (R)", "Circular Beam (CI)", "Hollow-Circular Beam (HC)", "I-Beam (I)", "T-Beam (T)", "C-Beam (C)", "Square Beam (S)")
)

A = 0
if cross_section_shape.startswith("Rectangular"):
    width = st.number_input("Width (m)", value=0.1)
    height = st.number_input("Height (m)", value=0.1)
    A = width * height
elif cross_section_shape.startswith("Circular"):
    radius = st.number_input("Radius (m)", value=0.05)
    A = np.pi * radius**2
elif cross_section_shape.startswith("Hollow-Circular"):
    outer_radius = st.number_input("Outer Radius (m)", value=0.06)
    inner_radius = st.number_input("Inner Radius (m)", value=0.04)
    if inner_radius >= outer_radius:
        st.error("Inner radius must be less than outer radius.")
    else:
        A = np.pi * (outer_radius**2 - inner_radius**2)
elif cross_section_shape.startswith("I-Beam"):
    width = st.number_input("Width (m)", value=0.1)
    height = st.number_input("Height (m)", value=0.2)
    flange_thickness = st.number_input("Flange Thickness (m)", value=0.02)
    web_thickness = st.number_input("Web Thickness (m)", value=0.01)
    A = (width * flange_thickness * 2) + (height - 2 * flange_thickness) * web_thickness
elif cross_section_shape.startswith("T-Beam"):
    width = st.number_input("Width (m)", value=0.1)
    height = st.number_input("Height (m)", value=0.15)
    flange_thickness = st.number_input("Flange Thickness (m)", value=0.02)
    web_thickness = st.number_input("Web Thickness (m)", value=0.01)
    A = (width * flange_thickness) + ((height - flange_thickness) * web_thickness)
elif cross_section_shape.startswith("C-Beam"):
    width = st.number_input("Width (m)", value=0.1)
    height = st.number_input("Height (m)", value=0.15)
    flange_thickness = st.number_input("Flange Thickness (m)", value=0.02)
    web_thickness = st.number_input("Web Thickness (m)", value=0.01)
    A = (width * flange_thickness * 2) + (height - 2 * flange_thickness) * web_thickness
elif cross_section_shape.startswith("Square"):
    side_length = st.number_input("Side Length (m)", value=0.1)
    A = side_length**2
else:
    st.warning("Invalid cross-sectional shape selected.")

k = E * A / l


forces = []
st.subheader("Compressive Force")
for n in range(int(i)):
    if n == i - 1:
        F_n = st.number_input(f"Force at Node {n+1} (N)", value=100.0)
    else:
        F_n = 0.0
    forces.append(F_n)

if st.button("Compute"):
    K = np.zeros((int(i), int(i)))
    for n in range(int(i) - 1):
        K[n, n]     += k
        K[n, n+1]   -= k
        K[n+1, n]   -= k
        K[n+1, n+1] += k

    F = np.array(forces)
    K[0, :] = 0
    K[0, 0] = 1
    F[0] = 0

    u = np.linalg.solve(K, F)
    st.write("### Nodal Displacements:")

    displacement_str = "    ".join([f"u{n} = {u[n]:.6f} m , " for n in range(int(i))])
    st.write(displacement_str)

    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.plot(range(int(i)), u, marker='o')
        ax1.set_title("Nodal Displacement vs Node Number")
        ax1.set_xlabel("Node Number")
        ax1.set_ylabel("Displacement (m)")
        ax1.grid(True)
        st.pyplot(fig1)

    with col2:
        num_nodes = len(u)
        x = np.linspace(0, l, num_nodes)
        y = np.zeros_like(x)
        y_disp = u

        fig2, ax2 = plt.subplots()
        line, = ax2.plot(x, y, 'o-', lw=2)
        ax2.set_ylim(min(y_disp)-0.01, max(y_disp)+0.01)
        ax2.set_xlim(0, l)
        ax2.set_xlabel("Beam Length (m)")
        ax2.set_ylabel("Displacement (m)")
        ax2.set_title("Animated Illustration of Beam Nodal Displacement")

        def animate(frame):
            alpha = frame / 20
            y_current = y + alpha * y_disp
            line.set_ydata(y_current)
            return line,

        ani = FuncAnimation(fig2, animate, frames=30, interval=50, blit=True)

        tmpfile = tempfile.NamedTemporaryFile(suffix='.gif', delete=False)
        ani.save(tmpfile.name, writer='pillow')
        plt.close(fig2)

        st.image(tmpfile.name, caption="Beam Nodal Displacement Animation")

st.write("If you have any questions or need further assistance, please feel free to ask!")
st.write("email: wiwatchumai@gmail.com")
st.write("instagram: @feuzzy_field")


    # Run the program: streamlit run app.py