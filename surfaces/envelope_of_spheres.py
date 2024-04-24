import bpy
import sympy as sp
import time
import sys
sys.path.append("C:\Program Files\Blender Foundation\Blender 4.0\4.0\scripts\modules\envelopes.py")
import envelopes as en
from mathutils import Vector
import importlib
importlib.reload(en)

start_time = time.time()

# Clear existing objects in scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Symbolic variable
t = sp.symbols('t')

# Read parameters from a text file
input_file = 'constant_radius/cornetto_constant_radius'
with open('C:/Users/tutko/Desktop/Masters-Thesis/surfaces/inputs/' + input_file + '.txt', 'r') as file:
    lines = file.readlines()

# Call the functions
curve_parametrization_str, radius_function_str = en.parse_parameters(lines)
curve_parametrization_exp, radius_function = en.convert_to_expressions(curve_parametrization_str, radius_function_str)
curve_parametrization = en.calculate_curve_parametrization(curve_parametrization_exp)
derivative_curve_parametrization = en.calculate_derivative_curve(curve_parametrization)
norm_derivative_curve_parametrization = en.calculate_norm_derivative_curve(derivative_curve_parametrization)
derivative_radius_function = en.calculate_derivative_radius(radius_function)
center_characteristic_curve = en.calculate_center_characteristic_curve(curve_parametrization, radius_function, derivative_radius_function, derivative_curve_parametrization, norm_derivative_curve_parametrization)
radius_characteristic_curve = en.calculate_radius_characteristic_curve(radius_function, derivative_radius_function, norm_derivative_curve_parametrization)

# Number of spheres to create with step and shift array
step = en.step(lines)
# Set the range of t values for the curve
t_values = en.t_values(lines, step)
number_of_spheres = en.number_of_spheres(t_values)

shift_array = en.shift_array(lines)

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
original_normal = Vector((0, 0, 1))

for i in range(number_of_spheres):
    # Circles with bridge edge loops
    bpy.ops.mesh.primitive_circle_add(radius=radii_char[i], location=f.shift_x(center_char[i], shift_array[-1]))
    circle_object = bpy.context.object

    rotated_normal_vector = Vector(derivatives[i])
    # Calculate rotation
    rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)

    # Apply the rotation
    circle_object.rotation_mode = 'AXIS_ANGLE'
    circle_object.rotation_axis_angle[0] = rotation_angle
    circle_object.rotation_axis_angle[1:] = rotation_axis

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.bridge_edge_loops()
bpy.ops.object.editmode_toggle()
   
for i in range(number_of_spheres):
    # Spheres
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radii[i], location=en.shift_x(points[i], shift_array[0]))
    bpy.ops.object.shade_smooth()
   
    # Circle
    bpy.ops.mesh.primitive_circle_add(radius=radii_char[i], location=en.shift_x(center_char[i], shift_array[1]))
    circle_object = bpy.context.object

    rotated_normal_vector = Vector(derivatives[i])
    # Calculate rotation
    rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)

    # Apply the rotation
    circle_object.rotation_mode = 'AXIS_ANGLE'
    circle_object.rotation_axis_angle[0] = rotation_angle
    circle_object.rotation_axis_angle[1:] = rotation_axis
    
#Update the scene
bpy.context.view_layer.update()
#Save the Blender file
bpy.ops.wm.save_as_mainfile(filepath='C:/Users/tutko/Desktop/Masters-Thesis/surfaces/outputs_envelope_of_spheres/' + input_file + '.blend') 

#Time computation
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")