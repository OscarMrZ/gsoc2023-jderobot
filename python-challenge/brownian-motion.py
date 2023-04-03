import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Robot:

    def __init__(self, arena_size, robot_radius, lin_speed, ang_speed):

        self.arena_size = arena_size
        self.robot_radius = robot_radius
        self.position = np.array([arena_size/2, arena_size/2])
        self.direction = np.array([1.0, 0.0])
        self.lin_speed = lin_speed
        self.ang_speed = ang_speed

        self.rot = 0
        self.turning = False
        self.turninit = False
        self.rot_angle = 0
        
    def move(self):
        
        # Move or turn the robot depending on the state
        if (not self.turning):
            self.position += self.direction * self.lin_speed
        else:
            # Initialize the random angle
            if (not self.turninit):
                self.turninit = True
                self.rot_angle = np.random.uniform(0.25*2*np.pi, 0.75*2*np.pi)
                self.rot_angle += self.rot

            # Turn the robot until it reaches the random angle
            if (self.rot < self.rot_angle):
                self.rot += self.ang_speed
                self.direction = np.array([np.cos(self.rot), np.sin(self.rot)])
            else:
                self.turning = False
                self.turninit = False

        # Handle the boundary conditions considering the robot radius
        if self.position[0] < self.robot_radius:
            self.position[0] = self.robot_radius
            self.turning = True
        elif self.position[0] > self.arena_size - self.robot_radius:
            self.position[0] = self.arena_size - self.robot_radius
            self.turning = True
        
        if self.position[1] < self.robot_radius:
            self.position[1] = self.robot_radius
            self.turning = True
        elif self.position[1] > self.arena_size - self.robot_radius:
            self.position[1] = self.arena_size - self.robot_radius
            self.turning = True

class BrownianRobotSimulation:

    def __init__(self, arena_size, lin_speed, ang_speed):
        
        self.robot = Robot(arena_size, 1, lin_speed, ang_speed)

        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim([0, arena_size])
        self.ax.set_ylim([0, arena_size])
        self.ax.set_aspect('equal')

        self.robot_circle = plt.Circle(self.robot.position, radius=1, color='r')
        self.arrow = plt.arrow(self.robot.position[0], self.robot.position[1], self.robot.direction[0], self.robot.direction[1], color='b', width=0.3)
        self.ax.add_artist(self.robot_circle)
        
    def update(self, i):

        # Move the robot
        self.robot.move()
        
        # Update the robot circle
        self.robot_circle.center = self.robot.position

        # Update the arrow
        self.arrow.remove()
        self.arrow = plt.arrow(self.robot.position[0], self.robot.position[1], self.robot.direction[0], self.robot.direction[1], color='b', width=0.3)
        self.ax.add_artist(self.arrow)

        return [self.robot_circle, self.arrow]
    
    def simulate(self, num_steps):
        ani = FuncAnimation(self.fig, self.update, frames=num_steps, interval=50, blit=True)
        plt.show()
        
if __name__ == '__main__':
    rsim = BrownianRobotSimulation(50, 0.5, 0.2)
    rsim.simulate(200)
