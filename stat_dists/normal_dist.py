__author__ = 'nunoe'

import random
import pylab


def plot_normal_dist(mean, sd, num_samples):
    """ Plots a histogram of a sample taken from a normal distribution of given parameters
    :param mean: float, the mean of the distribution
    :param sd: float, the standard deviation of the distribution
    :param num_samples: int, the total amount of samples taken from the distribution
    """
    samples = [random.gauss(mean, sd) for i in range(num_samples)]
    pylab.hist(samples, bins=101)
    pylab.show()


if __name__ == '__main__':
    plot_normal_dist(0, 1, 100000)