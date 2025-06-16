import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Damped system are required to calculate for the frequency response
# This script calculates the frequency response of a damped system

# 1. Free Vibration (Undamped/ Damped)
# 2. Forced Vibration (Undamped/ Damped)


# Define symbols
x = sp.symbols('x')
y = sp.Function('y')
# Example coefficients and forcing function
A, B, C = sp.symbols('A B C')
f = sp.Function('f')(x)

def function(x, A, B, C):
    ode = sp.Eq(A*y(x).diff(x, 2) + B*y(x).diff(x) + C*y(x), f)
    return ode

print("the equation is Ay''[x] + By'[x] + Cy[x] = f(x)")
print("Please input all the coefficients")
# Solve the ODE
A = float(input("Enter coefficient 'A':"))
B = float(input("Enter coefficient 'B':"))
C = float(input("Enter coefficient 'C':"))

damp_ratio= B / (2 * np.sqrt(A * C))
print(f"Damping ratio (ζ): {damp_ratio:.3f}")
# Determine the damping condition
if damp_ratio < 1:
    print("The system is underdamped")
elif damp_ratio == 1:
    print("The system is critically damped")    
else:
    print("The system is overdamped")  

ODE = function(x, A, B, C)
solution = sp.dsolve(ODE, y(x))
#sp.pprint(solution) is used to pretty print the solution
sp.pprint(solution)

# Frequency range
w = np.linspace(0, 10, 500)
# Complex frequency variable, j== sqrt(-1)
jw = 1j * w

# Frequency response H(jw)
H = 1 / (jw**2 + B * jw + C)

# Natural frequency
omega_n = np.sqrt(C / A)
print(f"Natural frequency (ω_n): {omega_n:.3f} rad/s")

# Plot magnitude
plt.plot(w, np.abs(H))
plt.title('Frequency Response Plot')
plt.xlabel('Frequency (rad/s)')
plt.ylabel('|H(jω)|')
plt.grid(True)
plt.show()