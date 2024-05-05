import numpy as np
from utils.shank_calculations.shankAngleCalculate import shankAngleCalculate

def shankAngleCalculationProcess(rightAnkleArray, rightKneeArray):
    horizontal_offset = 200

    # Calculate the coordinates of the reference point
    reference_point = np.array([rightAnkleArray[0] + horizontal_offset, rightAnkleArray[1], rightAnkleArray[2]])
            
    # Calculate vectors representing shank and the line from ankle to reference point
    shank_vector = rightAnkleArray - rightKneeArray
    reference_vector = reference_point - rightAnkleArray
            
    # Calculate angle between shank and the line from ankle to reference point
    angle = shankAngleCalculate(shank_vector, reference_vector)

    return angle