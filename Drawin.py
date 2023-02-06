import pygame
from math import *


class Drawin:
    # class wide variables
    robot_size = 12 # robot size
    robot_color = (73, 146, 104) # robot color
    pathcolor = (40, 45, 50)
    pathcolor2 = (80, 90, 100)
    particle_color = (180, 101, 74)
    # Vector image of a robot
    robot_Template = [(0.6, 0), (0, 0.2), (-0.2, 0.5), (-0.4, 0.2), (-0.4, -0.2), (-0.2, -0.5), (0, -0.2), (0.6, 0)]
    # Actual parameters
    world_size = 400
    landmarks  = [[20.0, 20.0], [380.0, 580.0], [20.0, 380.0], [380.0, 20.0]]
    cellSize = 50
    backgroundColor = (214, 217, 207)
    delimiterColor = (234, 237, 237)
    feature_size = 30
    feature_color = (32, 42, 68)
    feature_Template = [(-0.25, -0.5), (0.25, -0.5), (0.5, -0.25), (0.5, 0.25), (0.25, 0.5), (-0.25, 0.5), (-0.5, 0.25), (-0.5, -0.25)]


    @staticmethod
    def clear(screenHandle):
        screenHandle.fill(Drawin.backgroundColor)
        horizontalLen = 600 // Drawin.cellSize
        verticalLen = 400 // Drawin.cellSize
        for hor in range(1, verticalLen):
            pygame.draw.aalines(screenHandle, Drawin.delimiterColor, False,
                                ((0, Drawin.cellSize * hor - 1), (600, Drawin.cellSize * hor - 1)))
            pygame.draw.aalines(screenHandle, Drawin.delimiterColor, False,
                                ((0, Drawin.cellSize * hor), (600, Drawin.cellSize * hor)))
        for ver in range(1, horizontalLen):
            pygame.draw.aalines(screenHandle, Drawin.delimiterColor, False,
                                ((Drawin.cellSize * ver - 1, 0), (Drawin.cellSize * ver - 1, 400)))
            pygame.draw.aalines(screenHandle, Drawin.delimiterColor, False,
                                ((Drawin.cellSize * ver, 0), (Drawin.cellSize * ver, 400)))


    @staticmethod
    def draw(screenHandle, rob, part):
        # Draw solution
        partGrid = Drawin.getGrid(part)
        if len(part.path) > 1:
            pygame.draw.aalines(screenHandle, Drawin.pathcolor2, False, part.path)
        pygame.draw.aalines(screenHandle, Drawin.particle_color, True, partGrid)

        # Draw robot's true location
        robotGrid = Drawin.getGrid(rob)
        if len(rob.path) > 1 and rob.particle == False:
            pygame.draw.aalines(screenHandle, Drawin.pathcolor, False, rob.path)
        pygame.draw.aalines(screenHandle, Drawin.robot_color, True, robotGrid)
        pygame.draw.polygon(screenHandle, Drawin.robot_color, robotGrid, 0)

        # essential
        pygame.display.update()


    @staticmethod
    def getGrid(part):
        bodyVector = list(Drawin.robot_Template)
        robotGrid = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        for point in range(0, 8):
            robotGrid[point] = \
                ((bodyVector[point][0] * cos(part.orientation) - bodyVector[point][1] * sin(part.orientation)) * Drawin.robot_size + part.x,
                  (bodyVector[point][0] * sin(part.orientation) + bodyVector[point][1] * cos(part.orientation)) * Drawin.robot_size + part.y)
        return robotGrid
