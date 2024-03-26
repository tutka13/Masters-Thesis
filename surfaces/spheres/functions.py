import numpy as np
import sympy as sp

def find_rotation(normal_vector, rotated_normal_vector):
    """
    Finds the rotation angle and axis between two normal vectors.
    Input:
        normal_vector: The normal vector of the original circle.
        rotated_normal_vector: The normal vector of the rotated circle.
    Output:
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
    
# Shift on the x-axis - used in surface construction
def shift_x(parametrization, c):
    x = parametrization[0] + c
    y = parametrization[1]
    z = parametrization[2]
    return x, y, z

# Symbolic variable
t = sp.symbols('t')

#Reading from file and conversion to string
def parse_parameters(lines):
    curve_parametrization_str = lines[0].split(': ')[1].strip()
    radius_function_str = lines[1].split(': ')[1].strip()
    return curve_parametrization_str, radius_function_str

#Conversion to expressions
def convert_to_expressions(curve_parametrization_str, radius_function_str):
    curve_parametrization_exp = sp.sympify(curve_parametrization_str)
    radius_function = sp.sympify(radius_function_str)
    return curve_parametrization_exp, radius_function

#Calculation of parametrization
def calculate_curve_parametrization(curve_parametrization_exp):
    curve_parametrization = sp.Matrix([curve_parametrization_exp[0], curve_parametrization_exp[1], curve_parametrization_exp[2]])
    print("Curve Parametrization:", curve_parametrization)
    return curve_parametrization

#Calculation of derivative curve parametrization
def calculate_derivative_curve(curve_parametrization):
    derivative_curve_parametrization = sp.Matrix([sp.diff(coord, t) for coord in curve_parametrization])
    print("Derivative Curve Parametrization:", derivative_curve_parametrization)
    return derivative_curve_parametrization

#Calculation of derivative radius function
def calculate_derivative_radius(radius_function):
    derivative_radius_function = sp.diff(radius_function, t)
    print("Derivative Radius Function:", derivative_radius_function)
    return derivative_radius_function

#Calculation of norm of derivative curve parametrization
def calculate_norm_derivative_curve(derivative_curve_parametrization):
    norm_derivative_curve_parametrization = sp.sqrt(derivative_curve_parametrization[0]**2 + derivative_curve_parametrization[1]**2 + derivative_curve_parametrization[2]**2)
    print("Norm of Derivative Curve Parametrization:", norm_derivative_curve_parametrization)
    return norm_derivative_curve_parametrization

#Calculation of center characteristic curve
def calculate_center_characteristic_curve(curve_parametrization, radius_function, derivative_radius_function, derivative_curve_parametrization, norm_derivative_curve_parametrization):
    factor = radius_function * derivative_radius_function / norm_derivative_curve_parametrization**2
    center_characteristic_curve = curve_parametrization - factor * derivative_curve_parametrization
    print("Center of Characteristic Curve:", center_characteristic_curve)
    return center_characteristic_curve

#Calculation of radius characteristic curve
def calculate_radius_characteristic_curve(radius_function, derivative_radius_function, norm_derivative_curve_parametrization):
    factor = derivative_radius_function**2 / norm_derivative_curve_parametrization**2
    radius_characteristic_curve = sp.sqrt(radius_function**2 * (1 - factor))
    print("Radius of Characteristic Curve:", radius_characteristic_curve)
    return radius_characteristic_curve

# Parsing parameters and converting to appropriate data type
def number_of_spheres(lines):
    number_of_spheres_str = lines[3].split(': ')[1].strip()
    number_of_spheres = int(number_of_spheres_str)
    print("Number of spheres:", number_of_spheres)
    return number_of_spheres

def step(lines): 
    step_str = lines[4].split(': ')[1].strip()
    step = float(step_str)
    print("Step size:", step)
    return step 

def shift_array(lines):
    parts = lines[6].split(': ')[1].strip()
    # Split the values based on the delimiter (',')
    values_list = parts.split(',')
    # Convert the values to integers
    values = [int(value) for value in values_list]
    shift_array = np.arange(values[0], values[1], values[2])
    print("Shift array:", shift_array)
    return shift_array
