__author__ = 'nunoe'

import location
import field
import drunk
import numpy
import pylab


def walk(f, d, num_steps):
    start = f.get_loc(d)
    for s in range(num_steps):
        f.move_drunk(d)
    return start.dist_from(f.get_loc(d))


def sim_walks(num_steps, num_trials, drunk_class):
    homer = drunk_class('Homer')
    origin = location.Location(0, 0)
    distances = []

    for t in range(num_trials):
        f = field.Field()
        f.add_drunk(homer, origin)
        distances.append(walk(f, homer, num_steps))
    return distances


def drunk_tests(num_trials):
    for num_steps in [10, 100, 1000, 10000, 100000]:
        distances = sim_walks(num_steps, num_trials)
        print
        print 'Random walk of ' + str(num_steps) + ' steps'
        print 'Mean = ' + str(numpy.mean(distances))
        print 'Max = ' + str(max(distances)) + ', Min = ' + str(min(distances))


def drunk_test_plot(num_trials):
    steps_taken = [10, 100, 1000, 10000]
    mean_distances = []
    for num_steps in steps_taken:
        distances = sim_walks(num_steps, num_trials)
        mean_distances.append(numpy.mean(distances))

    pylab.plot(steps_taken, mean_distances)
    pylab.title('Mean distance from origin')
    pylab.xlabel('Steps Taken')
    pylab.ylabel('Steps from Origin')
    pylab.show()


def drunk_test_plot_sqrt(num_trials):
    steps_taken = [10, 100, 1000, 10000]
    mean_distances = []
    square_root_steps = []
    for num_steps in steps_taken:
        distances = sim_walks(num_steps, num_trials, drunk.UsualDrunk)
        mean_distances.append(numpy.mean(distances))
        square_root_steps.append(numpy.sqrt(num_steps))

    pylab.plot(steps_taken, mean_distances, 'b-', label='Mean distance')
    pylab.plot(steps_taken, square_root_steps, 'g-.', label='Square root of steps')
    pylab.title('Mean distance from origin')
    pylab.xlabel('Steps Taken')
    pylab.ylabel('Steps from Origin')
    pylab.legend(loc='upper left')
    pylab.show()


def drunk_test_plot_drunkentypes(num_trials):
    steps_taken = [10, 100, 1000, 10000]

    for drunk_class in (drunk.UsualDrunk, drunk.ColdDrunk, drunk.EDrunk):
        mean_distances = []

        for num_steps in steps_taken:
            distances = sim_walks(num_steps, num_trials, drunk.UsualDrunk)
            mean_distances.append(numpy.mean(distances))

        pylab.plot(steps_taken, mean_distances, label=drunk_class.__name__)
        pylab.title('Mean distance from origin')
        pylab.xlabel('Steps Taken')
        pylab.ylabel('Steps from Origin')
        pylab.legend(loc='upper left')
    pylab.show()


if __name__ == '__main__':
    drunk_test_plot_drunkentypes(50)