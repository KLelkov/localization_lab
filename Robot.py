import random
from math import *

world_size_x = 600
world_size_y = 400
landmarks = [[60, 340], [460, 180]]

class Robot:
    # class wide variables
    particle = False # particle flag, particles should have a different visuals
    path = [] # used to store the robot's traveled path
    # Actual parameters
    x = 0.0
    y = 0.0
    orientation = 0.0


    def __init__(self, particle = False):
        self.x = random.random() * 600
        self.y = random.random() * 400
        self.orientation = random.random() * 2.0 * pi
        self.wheels_noise = 0.0
        self.sense_len_noise = 0.0
        self.sense_ang_noise = 0.0
        # Graphic stuff
        self.path = []
        self.path.append((self.x, self.y))
        self.particle = particle


    def set(self, new_x, new_y, new_orientation):
        #new_x %= world_size    # cyclic truncate
        #new_y %= world_size
        new_orientation %= 2*pi
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
        self.path = []
        self.path.append((self.x, self.y))

    def sense(self):
        Z = []
        dd = sqrt((landmarks[1][0] - landmarks[0][0])**2 + (landmarks[1][1] - landmarks[0][1])**2)
        # get distances
        for i in range(len(landmarks)):
            d = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            d += random.gauss(0.0, self.sense_len_noise)
            a = atan2(landmarks[i][1] - self.y, landmarks[i][0] - self.x) - self.orientation
            a += random.gauss(0.0, self.sense_ang_noise)
            Z.append(d)
            Z.append(a % (2*pi))
        # Check if the measurements allow to build a valid solution
        while Z[0] + Z[2] <= dd:
            print("whhopsie")
            Z[0] += self.sense_len_noise / 6
            Z[2] += self.sense_len_noise / 6
        return Z

    def set_noise(self, new_w_noise, new_sd_noise, new_sa_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.wheels_noise = float(new_w_noise)
        self.sense_len_noise = float(new_sd_noise)
        self.sense_ang_noise = float(new_sa_noise)

    def move(self, left, right, time):
        # turn, and add randomness to the turning command
        left += random.gauss(0.0, self.wheels_noise)
        right += random.gauss(0.0, self.wheels_noise)
        rate = 0.15 * (left - right) / 2 / 0.5
        vel = 0.15 * (left + right) / 2
        #print("d --- {} {}".format(vel, rate))
        print("{:.1f} {:.1f} {:.1f}".format(left, right, time))

        x = self.x
        y = self.y
        orientation = self.orientation
        for i in range(0, int(time * 10)):
            orientation += rate * 0.1
            orientation %= 2 * pi
            dist = vel * 0.1
            xd = (cos(orientation) * dist)
            yd = (sin(orientation) * dist)
            x = max(min(599, (x + xd)), 0)
            y = max(min(399, (y + yd)), 0)
            self.path.append((x, y))
        #print(x)

        #print(self.x)
        part = Robot(self.particle)
        part.set_noise(self.wheels_noise, self.sense_len_noise, self.sense_ang_noise)
        part.set(x, y, orientation)
        part.path = self.path
        return part


    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


    def measurement_prob(self, measurement):
        # calculates how likely a measurement should be
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob


    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

    @staticmethod
    def eval(r, p):
        # find weights
        z = r.sense()
        w = []
        for i in range(0, len(p)):
            w.append(p[i].measurement_prob(z))
        s = sum(w)
        a = []
        for i in range(0, len(p)):
            a.append(w[i] / s)

        # find weighter sum
        s = 0.0
        for i in range(len(p)): # calculate mean error
            dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
            dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
            err = sqrt(dx * dx + dy * dy)
            s += err * a[i]
        return s
