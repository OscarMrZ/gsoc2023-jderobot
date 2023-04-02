from GUI import GUI
from HAL import HAL
from MAP import MAP
import numpy as np
from queue import PriorityQueue
import math
import time

# Path planning
planning_fase = True
MAX_DIST = 600
path = []
finding_yaw = True
SEARCH_AREA = 5
INC_AREA = 4

# Increases the value of the obstacles and adjacent points
def increase_obs_value(matrix, obstacles):
    
    for obs in obstacles:
        for x in range(-INC_AREA, INC_AREA):
            for y in range(-INC_AREA, INC_AREA):
                
                coord = (obs[0]+x, obs[1]+y)
                
                # Control matrix bounds
                if (coord[1] >= 400 or coord[0] >= 400): continue
                elif (coord[1] <= 0 or coord[0] <= 0): continue
                
                # Thicken the wall
                matrix[coord[1]][coord[0]] = 1

# Fills a matrix with the cost values, expanding from the goal until the dest is reached
def generate_gradient(map_img, origin, target):
    
    # Matrix to be filled
    matrix = np.full((400, 400), np.inf)
    
    frontier = PriorityQueue()
    obstacles = []
    
    # Initialize the first node
    matrix[target[1]][target[0]] = 0
    frontier.put((0, target))
    
    # Found a route from target to origin
    while not frontier.empty():
        
        node = frontier.get()
        
        # Get the coords and the previous distance
        pre_dist = node[0]
        coords = node[1]
        
        # Check if the origin has been found
        if (coords[1] == origin[1] and coords[0] == origin[0]): 
            break
        
        # If the node is an obstacle, it is saved and the propagation ends
        if (map_img[coords[1]][coords[0]] == 0): 
            obstacles.append(coords)
            continue
        
        # Assign weight depending if the succesor is next to the point or diagonal
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                
                # If it is the current point ignore
                if ((x, y) == (0, 0)): continue
                
                succ = (coords[0]+x, coords[1]+y)
                
                # Control matrix bounds
                if (succ[1] >= 400 or succ[0] >= 400): continue
                elif (succ[1] <= 0 or succ[0] <= 0): continue
                
                # If the value hasn't been set
                if (matrix[succ[1]][succ[0]] == np.inf):
                    
                    # Check if side or diagonal succ
                    if (abs(x) == abs(y)): new_dist = pre_dist + 1.4
                    else: new_dist = pre_dist + 1
                    
                    if (new_dist > MAX_DIST): new_dist = MAX_DIST
                        
                    # Assign the normalized value to the matrix
                    matrix[succ[1]][succ[0]] = new_dist / MAX_DIST
                    frontier.put((new_dist, succ))
                        
    # Delete every np.inf remaining = impassable obstacle
    for x in range(400):
        for y in range(400):
            if (matrix[y][x] == np.inf): matrix[y][x] = 1
            
    # Increase the weight of obstacles and adjacent points 
    increase_obs_value(matrix, obstacles)
    
    return matrix

# Gets a path following the gradient downwards
def path_from_gradient(matrix, origin, target):
    
    # Initialize the search
    coord = origin
    min_point = coord
    min_value = matrix[coord[1]][coord[0]]

    path = []
    
    while (coord[0] != target[0] or coord[1] != targ
