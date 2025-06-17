import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("OpenBeam: Axial Load Calculator")

E = st.number_input("Young's Modulus (E) [Pa]", value=200e6)
rho = st.number_input("Density (rho) [kg/m³]", value=7800.0)
A = st.number_input("Cross-sectional Area (A) [m²]", value=0.005)
l = st.number_input("Beam Length (l) [m]", value=1.0)
i = st.number_input("Number of Nodes", value=4, min_value=2, step=1)

k = E * A / l

forces = []
st.subheader("Forces")
for n in range(int(i)):
    if n == i - 1:
        F_n = st.number_input(f"Force at Node {n+1}", value=100.0)
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
    u = np.linalg.solve(K, F)
    st.write("### Nodal Displacements:")

    displacement_str = "      ".join([f"u{n} = {u[n]:.6f} m , " for n in range(int(i))])
    st.write(displacement_str)

    fig, ax = plt.subplots()
    ax.plot(range(int(i)), u, marker='o')
    ax.set_title("Nodal Displacement vs Node Number")
    ax.set_xlabel("Node Number")
    ax.set_ylabel("Displacement (m)")
    ax.grid(True)
    st.pyplot(fig)


    # Run the program: streamlit run app.py

