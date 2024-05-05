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
text_file = 'parabola_constant_radius'
with open('C:/Users/tutko/Desktop/Masters-Thesis/surfaces/inputs/constant_radius/' + text_file + '.txt', 'r') as file:
    lines = file.readlines()

# Call the functions
curve_parametrization_str, radius_function_str = en.parse_parameters(lines)
curve_parametrization_exp, radius_function = en.convert_to_expressions(curve_parametrization_str, radius_function_str)

curve_parametrization = en.calculate_curve_parametrization(curve_parametrization_exp)
derivative_curve_parametrization = en.calculate_derivative_curve(curve_parametrization)

norm_derivative_curve_parametrization = en.calculate_norm_derivative_curve(derivative_curve_parametrization)
curvature = en.curvature(derivative_curve_parametrization)
rho = en.rho(derivative_curve_parametrization, norm_derivative_curve_parametrization, a, b)
normal_vector_of_plane = en.normal_vector_of_plane(derivative_curve_parametrization)

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

rhos = []
normal_vectors_of_plane = []

# Parameter preparation
for t_value in t_values:
    # Substitute t_value
    curve_point = [expr.subs(t, t_value) for expr in curve_parametrization]
    #print("Curve Parametrization:", curve_point)

    derivative_curve_at_point = [expr.subs(t, t_value) for expr in derivative_curve_parametrization]
    #print("Derivative Curve Parametrization:", derivative_curve_at_point)

    curvature_at_point = curvature.subs(t, t_value)

    rhos_at_point = rho.sub(t, t_value)
    
    normal_vector_at_point = normal_vector_of_plane.subs(t, t_value)

    # Append to the lists
    points.append(curve_point)
    derivatives.append(derivative_curve_at_point)
    curvatures.append(curvature_at_point)

    rhos.append(rhos_at_point)
    normal_vectors_of_plane.append(normal_vector_at_point)
    #print(f'curvature: {curvature_at_point}')

#Define the original normal vector (assuming z-axis) 
original_normal = Vector((0, 0, 1)) 

#Ellipsoids
'''for i in range(number_of_ellipsoids):
    bpy.ops.mesh.primitive_uv_sphere_add(scale=(b, b, a), location=en.shift_x(points[i], shift_array[-1]))
    ellipsoid = bpy.context.object
    ellipsoid.name = "Ellipsoid"
    direction = Vector(derivatives[i])
    ellipsoid.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()'''

    #Planes
'''for i in range(number_of_ellipsoids):
    # planes for circles
    mesh = bpy.data.meshes.new(name="ArrowMesh")
    arrow = bpy.data.objects.new("ArrowObject", mesh)
    bpy.context.collection.objects.link(arrow)
    bpy.context.view_layer.objects.active = arrow
    arrow.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')

    # Create an arrow mesh (line and cone)
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.05, depth=0.2, location=(0, 0, 0.5))
    #arrow = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.025, depth=1, location=(0, 0, 0))

    bpy.ops.object.mode_set(mode='OBJECT')
    # Set the vector for the arrow
    arrow.scale = (2, 2, 2)
    rotated_vector = Vector(derivatives[i])
    # Calculate rotation
    rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_vector)
    # Apply the rotation
    arrow.rotation_mode = 'AXIS_ANGLE'
    arrow.rotation_axis_angle[0] = rotation_angle
    arrow.rotation_axis_angle[1:] = rotation_axis
    arrow.location = center_char_circles[i]
    
    if (abs(rhos[i]) >= abs(b)):
        bpy.ops.mesh.primitive_plane_add(location=points[i])
        plane = bpy.context.object
        plane.name = "PlaneCircles"
        
        rotated_vector = Vector(derivatives[i])
        rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_vector)
        # Apply the rotation
        plane.rotation_mode = 'AXIS_ANGLE'
        plane.rotation_axis_angle[0] = rotation_angle
        plane.rotation_axis_angle[1:] = rotation_axis

#Planes    
for i in range(number_of_ellipsoids):
    #roviny pre elipsy
    mesh = bpy.data.meshes.new(name="ArrowMesh")
    arrow = bpy.data.objects.new("ArrowObject", mesh)
    bpy.context.collection.objects.link(arrow)
    bpy.context.view_layer.objects.active = arrow
    arrow.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')

    # Create an arrow mesh (line and cone)
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.05, depth=0.2, location=(0, 0, 0.5))
    #arrow = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.025, depth=1, location=(0, 0, 0))

    bpy.ops.object.mode_set(mode='OBJECT')
    # Set the vector for the arrow
    arrow.scale = (2, 2, 2)
    
    rotated_normal_vector = en.sympy_matrix_to_vector(normal_vectors_of_plane[i])
    # Calculate rotation
    rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)
    # Apply the rotation
    arrow.rotation_mode = 'AXIS_ANGLE'
    arrow.rotation_axis_angle[0] = rotation_angle
    arrow.rotation_axis_angle[1:] = rotation_axis
    arrow.location = center_char_circles[i]
    #+rhos[i]*normal_vectors_of_plane[i]
    if (abs(rhos[i]) < abs(b)):
        bpy.ops.mesh.primitive_plane_add(location=points[i])
        #+rhos[i]*normal_vectors_of_plane[i])
        plane = bpy.context.object
        plane.name = "PlaneEllipses"
        
        rotated_normal_vector = Vector(normal_vectors_of_plane[i])
        rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)
        # Apply the rotation
        plane.rotation_mode = 'AXIS_ANGLE'
        plane.rotation_axis_angle[0] = rotation_angle
        plane.rotation_axis_angle[1:] = rotation_axis'''
        
half = round(number_of_ellipsoids/2)
    
for i in range(half):         
    if (ratio >= curvatures[i]):
        bpy.ops.mesh.primitive_circle_add(radius=b, location=points[i])
        circle = bpy.context.object
        circle.name = "Circle"
        rotated_normal_vector = Vector(derivatives[i])
        # Calculate rotation
        rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)

        # Apply the rotation
        circle.rotation_mode = 'AXIS_ANGLE'
        circle.rotation_axis_angle[0] = rotation_angle
        circle.rotation_axis_angle[1:] = rotation_axis
        
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.bridge_edge_loops()
bpy.ops.object.editmode_toggle()

for i in range(half + 1):         
    if (abs(rhos[half + i]) >= abs(b)):
        bpy.ops.mesh.primitive_circle_add(location=points[half+i])
        circle = bpy.context.object
        circle.name = "Circle"
        rotated_normal_vector = Vector(derivatives[half + i])
        # Calculate rotation
        rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)

        # Apply the rotation
        circle.rotation_mode = 'AXIS_ANGLE'
        circle.rotation_axis_angle[0] = rotation_angle
        circle.rotation_axis_angle[1:] = rotation_axis

# Select circles
for o in bpy.data.objects:
    if o.name.startswith("Circle.0"):
        number = int(o.name.split(".")[1])
        if 2 <= number <= half:
            o.select_set(True)

bpy.ops.object.join()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.bridge_edge_loops()
bpy.ops.object.editmode_toggle()

for i in range(number_of_ellipsoids):
    if (ratio < curvatures[i]):
        bpy.ops.mesh.primitive_uv_sphere_add(scale=(b, b, a), location=points[i])
        ellipsoid = bpy.context.object
        ellipsoid.name = "Ellipsoid"
        direction = Vector((derivatives[i][0], derivatives[i][1], derivatives[i][2]))
        ellipsoid.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
        
        #Ellipses
        '''bpy.ops.mesh.primitive_circle_add(location=points[i]+rhos[i]*normal_vectors_of_plane[i])
        ellipse = bpy.context.object
        ellipse.name = "Ellipse"
        ellipse.scale.y = en.minor_axis(rhos[i], b)   # Resize along X-axis
        ellipse.scale.x = en.major_axis(rhos[i], a, b)  # Resize along Y-ax
             
        rotated_normal_vector = Vector(normal_vectors_of_plane[i])
        # Calculate rotation
        rotation_angle, rotation_axis = en.find_rotation(original_normal, rotated_normal_vector)
       
        # Apply the rotation
        ellipse.rotation_mode = 'AXIS_ANGLE'
        ellipse.rotation_axis_angle[0] = rotation_angle
        ellipse.rotation_axis_angle[1:] = rotation_axis'''         
    
#Update the scene
bpy.context.view_layer.update()
# Save the Blender file
#bpy.ops.wm.save_as_mainfile(filepath='C:/Users/tutko/Desktop/Masters-Thesis/surfaces/outputs_envelope_of_ellipsoids/process' + text_file + '.blend') 

#Time computation
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")