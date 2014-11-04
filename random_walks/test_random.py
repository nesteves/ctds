__author__ = 'nunoe'

import random


def generate_even():
    return random.choice(range(0, 100, 2))


print str(generate_even())