import bpy
import sympy as sp
import time
import sys
sys.path.append('C:/Program Files/Blender Foundation/Blender 4.0/4.0/scripts/modules')
import envelopes as en
from mathutils import Vector
import importlib
importlib.reload(en)

# Factors of scaling
a = 2
b = 1

start_time = time.time()

# Clear existing objects in scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Symbolic variable
t = sp.symbols('t')

# Read parameters from a text file
text_file = 'ellipse_constant_radius'
with open('C:/Users/tutko/Desktop/Masters-Thesis/surfaces/inputs/constant_radius/' + text_file + '.txt', 'r') as file:
    lines = file.readlines()

# Call the functions
curve_parametrization_str, radius_function_str = en.parse_parameters(lines)
curve_parametrization_exp, radius_function = en.convert_to_expressions(curve_parametrization_str, radius_function_str)

curve_parametrization = en.calculate_curve_parametrization(curve_parametrization_exp)
derivative_curve_parametrization = en.calculate_derivative_curve(curve_parametrization)

curvature = en.curvature(derivative_curve_parametrization)
ratio = en.ratio(a, b)
print(f'ratio: {ratio}')

# Number of ellipsoids to create with step and shift array
step = en.step(lines)
# Set the range of t values for the curve
t_values = en.t_values(lines, step)
number_of_ellipsoids = en.number_of_spheres(t_values)
shift_array = en.shift_array(lines)

# Compute the point, derivative at each point on the curve
points = []
derivatives = []

curvatures = []

# Parameter preparation
for t_value in t_values:
    # Substitute t_value
    curve_point = [expr.subs(t, t_value) for expr in curve_parametrization]
    #print("Curve Parametrization:", curve_point)

    derivative_curve_at_point = [expr.subs(t, t_value) for expr in derivative_curve_parametrization]
    #print("Derivative Curve Parametrization:", derivative_curve_at_point)
   
    curvature_at_point = curvature.subs(t, t_value)
    
    # Append to the lists
    points.append(curve_point)
    derivatives.append(derivative_curve_at_point)
    curvatures.append(curvature_at_point)
    #print(f'curvature: {curvature_at_point}')

#Define the original normal vector (assuming z-axis) 
original_normal = Vector((0, 0, 1)) 

# Ellipsoids
for i in range(number_of_ellipsoids):
    bpy.ops.mesh.primitive_uv_sphere_add(scale=(b, b, a), location=en.shift_x(points[i], shift_array[0]))
    ellipsoid = bpy.context.object
    ellipsoid.name = "Ellipsoid"
    direction = Vector(derivatives[i])
    ellipsoid.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()

# Ellipsoids + circles        
for i in range(number_of_ellipsoids):   
    if (ratio >= curvatures[i]):  
        bpy.ops.mesh.primitive_circle_add(radius=b, location=en.shift_x(points[i], shift_array[1]))
        circle = bpy.context.object
        circle.name = "Circle"
        rotated_normal_vector = Vector(derivatives[i])
        # Calculate rotation
        rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)

        # Apply the rotation
        circle.rotation_mode = 'AXIS_ANGLE'
        circle.rotation_axis_angle[0] = rotation_angle
        circle.rotation_axis_angle[1:] = rotation_axis        

for i in range(number_of_ellipsoids):
    if (ratio < curvatures[i]):
        bpy.ops.mesh.primitive_uv_sphere_add(scale=(b, b, a), location=en.shift_x(points[i], shift_array[1]))
        ellipsoid = bpy.context.object
        ellipsoid.name = "Ellipsoid"
        direction = Vector(derivatives[i])
        ellipsoid.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()       

# Envelope    
for i in range(number_of_ellipsoids):    
    if (ratio >= curvatures[i]):  
        bpy.ops.mesh.primitive_circle_add(radius=b, location=en.shift_x(points[i], shift_array[2]))
        circle = bpy.context.object
        circle.name = "Circle"
        rotated_normal_vector = Vector(derivatives[i])
        # Calculate rotation
        rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)

        # Apply the rotation
        circle.rotation_mode = 'AXIS_ANGLE'
        circle.rotation_axis_angle[0] = rotation_angle
        circle.rotation_axis_angle[1:] = rotation_axis        

for i in range(number_of_ellipsoids):
    if (ratio < curvatures[i]):
        bpy.ops.mesh.primitive_uv_sphere_add(scale=(b, b, a), location=en.shift_x(points[i], shift_array[2]))
        ellipsoid = bpy.context.object
        ellipsoid.name = "Ellipsoid"
        direction = Vector(derivatives[i])
        ellipsoid.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
                    
#Update the scene
bpy.context.view_layer.update()
# Save the Blender file
#bpy.ops.wm.save_as_mainfile(filepath='C:/Users/tutko/Desktop/Masters-Thesis/surfaces/outputs_envelope_of_ellipsoids/ellipsoids_and_circles/' + text_file + '.blend') 

#Time computation
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")