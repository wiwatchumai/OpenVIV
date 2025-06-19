import numpy as np 
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define system type

# 1. Undamped Force Vibration (UFV)
# 2. Damped Force Vibration (DFV)
# 3. Undamped Free Vibration (UFV)
# 4. Damped Free Vibration (DFV)

system_type = input("Enter type of vibration system: ")

# 1. Rotor system (R)
# 2. External force system (EF)
# 3. Base excitation system (BE)

system_condition = input("Enter condition of vibration system: ")
t=sp.symbols('t')

if system_type == "UFV":
    if system_condition == "R":
        print("Undamped Force Vibration with Rotor system")
        # Define the equations of motion for the rotor system
        # Placeholder for actual equations
    if system_condition == "EF":
        print("Undamped Force Vibration with External force system")
        # Define the equations of motion for the external force system
        # Placeholder for actual equations
    if system_condition == "BE":
        print("Undamped Force Vibration with Base excitation system")
        # Define the equations of motion for the base excitation system
        # Placeholder for actual equations

if system_type == "DFV":
    if system_condition == "R":
        print("Damped Force Vibration with Rotor system")
        # Define the equations of motion for the rotor system
        # Placeholder for actual equations
    if system_condition == "EF":
        print("Damped Force Vibration with External force system")
        # Define the equations of motion for the external force system
        # Placeholder for actual equations
    if system_condition == "BE":
        print("Damped Force Vibration with Base excitation system")
        # Define the equations of motion for the base excitation system
        # Placeholder for actual equations

if system_type == "UFV":
    if system_condition == "R":
        print("Undamped Free Vibration with Rotor system")
        # Define the equations of motion for the rotor system
        # Placeholder for actual equations
    if system_condition == "EF":
        print("Undamped Free Vibration with External force system")
        # Define the equations of motion for the external force system
        # Placeholder for actual equations
    if system_condition == "BE":
        print("Undamped Free Vibration with Base excitation system")
        # Define the equations of motion for the base excitation system
        # Placeholder for actual equations