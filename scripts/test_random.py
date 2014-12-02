__author__ = 'nunoe'

import random
import pylab


def sample_quizzes(num_trials):
    scores = []
    for i in range(num_trials):
        mid1 = random.choice(range(50, 81)) * 0.25
        mid2 = random.choice(range(60, 91)) * 0.25
        exam = random.choice(range(55, 96)) * 0.50
        result = mid1 + mid2 + exam

        scores.append(result)

    return scores


def plot_scores():
    values = sample_quizzes(10000)
    pylab.hist(values, bins=7)
    pylab.xlabel('Final Score')
    pylab.ylabel('Number of Trials')
    pylab.title('Distribution of Scores')
    pylab.show()


def prob_test(limit):
    n = 0
    while (5.0 ** n) / (6.0 ** (n+1)) > limit:
        n += 1
    return n + 1


if __name__ == '__main__':
    # plot_scores()

    print prob_test(0.5)
    print prob_test(5.0/36)
    print prob_test(25.0/216)