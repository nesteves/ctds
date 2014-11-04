__author__ = 'nunoe'

import random


class Drunk(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'This drunk is named ' + self.name


class UsualDrunk(Drunk):
    def take_step(self):
        step_choices = [(0.0, 1.0), (0.0, -1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(step_choices)


class ColdDrunk(Drunk):
    def take_step(self):
        step_choices = [(0.0, 0.95), (0.0, -1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(step_choices)


class EDrunk(Drunk):
    def take_step(self):
        delta_x = random.random()
        if random.random() < 0.5:
            delta_x = -delta_x
        delta_y = random.random()
        if random.random() < 0.5:
            delta_y = -delta_y
        return delta_x, delta_x