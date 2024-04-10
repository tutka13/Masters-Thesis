import bpy
import sympy as sp
import time
import sys
sys.path.append("C:\Program Files\Blender Foundation\Blender 4.0\4.0\scripts\modules\functions.py")
import functions as f
from mathutils import Vector

start_time = time.time()

# Clear existing objects in scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Symbolic variable
t = sp.symbols('t')

# Factors of scaling
a = 1.5
b = 1

# Read parameters from a text file
text_file = 'cornetto_constant_radius'
with open('C:/Users/tutko/Desktop/Masters-Thesis/surfaces/inputs/constant_radius/' + text_file + '.txt', 'r') as file:
    lines = file.readlines()

# Call the functions
curve_parametrization_str, radius_function_str = f.parse_parameters(lines)
curve_parametrization_exp, radius_function = f.convert_to_expressions(curve_parametrization_str, radius_function_str)
curve_parametrization = f.calculate_curve_parametrization(curve_parametrization_exp)
derivative_curve_parametrization = f.calculate_derivative_curve(curve_parametrization)
norm_derivative_curve_parametrization = f.calculate_norm_derivative_curve(derivative_curve_parametrization)
derivative_radius_function = f.calculate_derivative_radius(radius_function)
center_characteristic_curve = f.calculate_center_characteristic_curve(curve_parametrization, 
radius_function, derivative_radius_function, derivative_curve_parametrization, norm_derivative_curve_parametrization)
radius_characteristic_curve = f.calculate_radius_characteristic_curve(radius_function, 
derivative_radius_function, norm_derivative_curve_parametrization)

# Number of ellipsoids to create with step and shift array
step = f.step(lines)
# Set the range of t values for the curve
t_values = f.t_values(lines, step)
number_of_ellipsoids = f.number_of_spheres(t_values)
shift_array = f.shift_array(lines)

# Compute the point, derivative at each point on the curve
points = []
derivatives = []
radii = []
# Compute the center and radius of characteristic circle
center_char = []
radii_char = []

# Parameter preparation
for t_value in t_values:
    # Substitute t_value
    curve_point = [expr.subs(t, t_value) for expr in curve_parametrization]
    #print("Curve Parametrization:", curve_point)

    derivative_curve_at_point = [expr.subs(t, t_value) for expr in derivative_curve_parametrization]
    #print("Derivative Curve Parametrization:", derivative_curve_at_point)

    radius_at_point = radius_function.subs(t, t_value)
    #print("Radius Function:", radius_at_point)

    center_characteristic_at_point = center_characteristic_curve.subs(t, t_value)
    #print("Center of Characteristic Curve:", center_characteristic_at_point)

    radius_characteristic_at_point = radius_characteristic_curve.subs(t, t_value)
    #print("Radius of Characteristic Curve:", radius_characteristic_at_point)

    # Append to the lists
    points.append(curve_point)
    derivatives.append(derivative_curve_at_point)
    radii.append(radius_at_point)

    center_char.append(center_characteristic_at_point)
    radii_char.append(radius_characteristic_at_point)

#Computation of rotation characteristic curves
#Define the original normal vector (assuming z-axis)
for i in range(number_of_ellipsoids): 
    # Ellipsoids with relevant scaling factors
    bpy.ops.mesh.primitive_uv_sphere_add(scale=(b, b, a), location=center_char[i])
    ellipsoid = bpy.context.object
    direction_a = Vector((derivatives[i][0], derivatives[i][1], derivatives[i][2]))
    ellipsoid.rotation_euler = direction_a.to_track_quat('Z', 'Y').to_euler()
      
#Update the scene
bpy.context.view_layer.update()
# Save the Blender file
#bpy.ops.wm.save_as_mainfile(filepath='C:/Users/tutko/Desktop/Masters-Thesis/surfaces/outputs_ellipsoids/' + text_file + '.blend') 

#Time computation
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")