import bpy
import math as m
import numpy as np
import sympy as sp
import time
from mathutils import Vector

start_time = time.time()

# Clear existing objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Symbolic variable
t = sp.symbols('t')

# Control points
P0 = [0, 2, 0]
P1 = [4, 1, 1]
P2 = [1, 0, 5]
P3 = [0, 3, 6]

# Bezier curve parametrization
x_t = (1 - t)**3 * P0[0] + 3 * (1 - t)**2 * t * P1[0] + 3 * (1 - t) * t**2 * P2[0] + t**3 * P3[0]
y_t = (1 - t)**3 * P0[1] + 3 * (1 - t)**2 * t * P1[1] + 3 * (1 - t) * t**2 * P2[1] + t**3 * P3[1]
z_t = (1 - t)**3 * P0[2] + 3 * (1 - t)**2 * t * P1[2] + 3 * (1 - t) * t**2 * P2[2] + t**3 * P3[2]

# Bezier curve parametrization expression
curve_parametrization_exp = [x_t, y_t, z_t]

# Read parameters from a text file
text_file = 'bezier'
with open('C:/Users/tutko/Desktop/Vysledne-plochy/' + text_file + '/' + text_file + '.txt', 'r') as file:
    lines = file.readlines()

# Parse parameters
#curve_parametrization_str = lines[0].split(': ')[1].strip()
radius_function_str = lines[0].split(': ')[1].strip()
radius_function = sp.sympify(radius_function_str)

# Convert symbolic expressions to sp.Matrix
curve_parametrization = sp.Matrix([curve_parametrization_exp[0], curve_parametrization_exp[1], curve_parametrization_exp[2]])

# Define the parametric equation for the curve
print("Curve Parametrization:", curve_parametrization)

# Derivative of the parametrization is the normal vector
derivative_curve_parametrization = sp.Matrix([sp.diff(coord, t) for coord in curve_parametrization])
print("Derivative Curve Parametrization:", derivative_curve_parametrization)

# Norm of the derivative vector
norm_derivative_curve_parametrization = sp.sqrt(derivative_curve_parametrization[0]**2 + derivative_curve_parametrization[1]**2 + derivative_curve_parametrization[2]**2)
print("Norm of Derivative Curve Parametrization:", norm_derivative_curve_parametrization)

# Define the function for the radius of the spheres
print("Radius Function:", radius_function)

# Derivative of the radius function
derivative_radius_function = sp.diff(radius_function, t)
print("Derivative of Radius Function:", derivative_radius_function)

# Calculate the center of the characteristic curve
factor = radius_function * derivative_radius_function / norm_derivative_curve_parametrization**2
center_characteristic_curve = curve_parametrization - factor * derivative_curve_parametrization
print("Center of Characteristic Curve:", center_characteristic_curve)

# Calculate the radius of the characteristic curve
subtraction = derivative_radius_function**2 / norm_derivative_curve_parametrization**2
radius_characteristic_curve = sp.sqrt(radius_function**2 * (1 - subtraction))
print("Radius of Characteristic Curve:", radius_characteristic_curve)

# Number of spheres to create
n_spheres = 100
step = 0.01

# Set the range of t values for the curve
t_values = np.arange(0, 1, step)

# Compute the point, derivative and norm of the derivative at each point on the curve
points = []
derivatives = []
norms = []
radii = []
derivatives_radii = []
center_char = []
radii_char = []

# Parameter preparation
for t_value in t_values:
    # Substitute t_value
    curve_point = [expr.subs(t, t_value) for expr in curve_parametrization]
    #print("Curve Parametrization:", curve_point)

    derivative_curve_at_point = [expr.subs(t, t_value) for expr in derivative_curve_parametrization]
    #print("Derivative Curve Parametrization:", derivative_curve_at_point)

    norm_at_point = norm_derivative_curve_parametrization.subs(t, t_value)
    #print("Norm of Derivative Curve Parametrization:", norm_at_point)

    radius_at_point = radius_function.subs(t, t_value)
    #print("Radius Function:", radius_at_point)
    
    derivative_radius_at_point = derivative_radius_function.subs(t, t_value)
    #print("Derivative of Radius Function:", derivative_radius_at_point)

    center_characteristic_at_point = center_characteristic_curve.subs(t, t_value)
    #print("Center of Characteristic Curve:", center_characteristic_at_point)

    radius_characteristic_at_point = radius_characteristic_curve.subs(t, t_value)
    #print("Radius of Characteristic Curve:", radius_characteristic_at_point)

    # Append to the lists
    points.append(curve_point)
    derivatives.append(derivative_curve_at_point)
    norms.append(norm_at_point)  

    radii.append(radius_at_point)
    derivatives_radii.append(derivative_radius_at_point)
    center_char.append(center_characteristic_at_point)
    radii_char.append(radius_characteristic_at_point)
    
def find_rotation(normal_vector, rotated_normal_vector):
    """
    Finds the rotation angle and axis between two normal vectors.

    Args:
        normal_vector: The normal vector of the original circle.
        rotated_normal_vector: The normal vector of the rotated circle.

    Returns:
        rotation_angle: The rotation angle (in radians).
        rotation_axis: The rotation axis.
    """
    # Normalize the input vectors
    normal_vector.normalize()
    rotated_normal_vector.normalize()

    # Find the rotation axis (cross product of normal vectors)
    rotation_axis = normal_vector.cross(rotated_normal_vector)
    rotation_axis.normalize()

    # Calculate the rotation angle (in radians)
    rotation_angle = normal_vector.angle(rotated_normal_vector)

    return rotation_angle, rotation_axis

shift_array = np.arange(-10, 11, 5)
# Shift on the x-axis - used in surface construction
def shift_x(parametrization, c):
    x = parametrization[0] + c
    y = parametrization[1]
    z = parametrization[2]
    return x, y, z

for i in range(n_spheres):
    # Kružnice s bridge edge loops
    bpy.ops.mesh.primitive_circle_add(radius=radii_char[i], location=shift_x(center_char[i], shift_array[0]))
    circle_object = bpy.context.object
    
    # Define the original normal vector (assuming z-axis)
    original_normal = Vector((0, 0, 1))
    rotated_normal_vector = Vector(derivatives[i])

    # Calculate rotation
    rotation_angle, rotation_axis = find_rotation(original_normal, rotated_normal_vector)

    # Apply the rotation
    circle_object.rotation_mode = 'AXIS_ANGLE'
    circle_object.rotation_axis_angle[0] = rotation_angle
    circle_object.rotation_axis_angle[1:] = rotation_axis

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.bridge_edge_loops()
bpy.ops.object.editmode_toggle()
   
for i in range(n_spheres):
    # Sféry
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radii[i], location=shift_x(points[i], shift_array[1]))
    bpy.ops.object.shade_smooth()

for i in range(n_spheres):    
    # Kružnice
    bpy.ops.mesh.primitive_circle_add(radius=radii_char[i], location=shift_x(center_char[i], shift_array[2]))
    circle_object = bpy.context.object
    
    # Define the original normal vector (assuming z-axis)
    original_normal = Vector((0, 0, 1))
    rotated_normal_vector = Vector(derivatives[i])

    # Calculate rotation
    rotation_angle, rotation_axis = find_rotation(original_normal, rotated_normal_vector)

    # Apply the rotation
    circle_object.rotation_mode = 'AXIS_ANGLE'
    circle_object.rotation_axis_angle[0] = rotation_angle
    circle_object.rotation_axis_angle[1:] = rotation_axis

for i in range(n_spheres):
    # Sféry a kružnice
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radii[i], location=shift_x(points[i], shift_array[1]))
    bpy.ops.object.shade_smooth()

    bpy.ops.mesh.primitive_circle_add(radius=radii_char[i], location=shift_x(center_char[i], shift_array[2]))
    circle_object = bpy.context.object
    
    # Define the original normal vector (assuming z-axis)
    original_normal = Vector((0, 0, 1))
    rotated_normal_vector = Vector(derivatives[i])

    # Calculate rotation
    rotation_angle, rotation_axis = find_rotation(original_normal, rotated_normal_vector)

    # Apply the rotation
    circle_object.rotation_mode = 'AXIS_ANGLE'
    circle_object.rotation_axis_angle[0] = rotation_angle
    circle_object.rotation_axis_angle[1:] = rotation_axis
         
#Update the scene
bpy.context.view_layer.update()
# Save the Blender file
bpy.ops.wm.save_as_mainfile(filepath='C:/Users/tutko/Desktop/Vysledne-plochy/' + text_file + '/' + text_file + '.blend') 

#Time computation
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
