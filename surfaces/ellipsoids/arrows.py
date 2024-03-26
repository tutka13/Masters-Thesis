import bpy
import sympy as sp
import time
import sys
sys.path.append("C:\Program Files\Blender Foundation\Blender 4.0\4.0\scripts\modules\functions.py")
import functions as f
from mathutils import Vector

start_time = time.time()

# Clear existing objects in the scenescript.py
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Symbolic variable
t = sp.symbols('t')

# Read parameters from a text file
text_file = 'helix_radius_function'
with open('C:/Users/tutko/Desktop/Vysledne-plochy/' + text_file + '/' + text_file + '.txt', 'r') as file:
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

# Number of spheres to create with step and shift array
step = f.step(lines)
# Set the range of t values for the curve
t_values = f.t_values(lines, step)
number_of_spheres = f.number_of_spheres(t_values)

shift_array = f.shift_array(lines)

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

for i in range(number_of_spheres):
    # Sféry
    #bpy.ops.mesh.primitive_uv_sphere_add(radius=radii[i], location=f.shift_x(points[i], shift_array[0]))
    #bpy.ops.object.shade_smooth()

    # sipky ako velkost derivacie
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
    vector = Vector((derivatives[i][0], derivatives[i][1], derivatives[i][2]))
    scale_factor = vector.length
    # Set the scale of the arrow based on the vector length, rotation of the arrow based on the vector direction, the location of the arrow 
    arrow.scale = (scale_factor, scale_factor, scale_factor)
    arrow.rotation_euler = vector.to_track_quat('Z', 'Y').to_euler()
    arrow.location = (center_char[i][0], center_char[i][1], center_char[i][2])
    
    '''a = 1.5
    bpy.ops.mesh.primitive_uv_sphere_add(scale=(1, 1, a))
    ellipsoid = bpy.context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    vector = Vector((derivatives[i][0], derivatives[i][1], derivatives[i][2]))
    #scale_factor = vector.length
    #ellipsoid.scale = (scale_factor, scale_factor, scale_factor)
    ellipsoid.rotation_euler = vector.to_track_quat('Z', 'Y').to_euler()
    ellipsoid.location = (center_char[i][0], center_char[i][1], center_char[i][2])'''
      
#Update the scene
bpy.context.view_layer.update()
# Save the Blender file
bpy.ops.wm.save_as_mainfile(filepath='C:/Users/tutko/Desktop/Vysledne-plochy/Elipsoidy/' + text_file + '_arrows' + '.blend') 

#Time computation
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")