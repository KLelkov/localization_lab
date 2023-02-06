import pygame, sys, random
from pygame.locals import *
from math import *
import Robot, Drawin

pygame.init()

screen = pygame.display.set_mode((600, 400), 0, 32)
pygame.display.set_caption("Particle filter simulation")

realRobot = Robot.Robot(False)
realRobot.set_noise(0.2, 10.0, 0.3)
simRobot = Robot.Robot(True)
simRobot.set_noise(0.2, 10.0, 0.3)
realRobot.set(300, 200, -pi/2)
simRobot.set(300, 200, -pi/2)

def predict(motion):
    a = 0
    # Place your prediction code here!

def correct(measurement):
    a = 1
    # Place your correction code here!



print("Input data:")
Z0 = realRobot.sense()
print(' '.join(['{0:0.1f}'.format(m) for m in Z0]))
realRobot = realRobot.move(80, 79.09, 23)
Z1 = realRobot.sense()
print(' '.join(['{0:0.1f}'.format(m) for m in Z1]))
realRobot = realRobot.move(80, 80, 11)
Z2 = realRobot.sense()
print(' '.join(['{0:0.1f}'.format(m) for m in Z2]))

print("")
print("Final real robot position:")
print("{:.1f} {:.1f} {:.1f}".format(realRobot.x, realRobot.y, realRobot.orientation * 180.0 / pi))

# Place yout localization algo here!
p = []
correct(Z0)
predict([80, 79.09, 23])
correct(Z1)
predict([80, 80, 11])
correct(Z2)

print("")
print("Final simualtion robot position:")
print("{:.1f} {:.1f} {:.1f}".format(simRobot.x, simRobot.y, simRobot.orientation * 180.0 / pi))


Drawin.Drawin.clear(screen)
Drawin.Drawin.draw(screen, realRobot, simRobot)

mainloop = True
while mainloop:
    for event in pygame.event.get():
        if event.type == QUIT:
            mainloop = False

pygame.quit()
