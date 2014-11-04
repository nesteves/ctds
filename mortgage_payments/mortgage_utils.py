__author__ = 'NLESTEVES'

import pylab


def compare_mortgages(amount, years, fixed_rate, points, points_rate,
                      var_rate1, var_rate2, var_months):
    """ Function used to compare 3 mortgage options derived from the saem loaned amount
    :param amount: float, total amount of the loan
    :param years: int, number of years to pay the loan in
    :param fixed_rate: float, the annual fixed rate to apply to the remaining principal
    :param points: float, annual interest rate for a loan with points
    :param points_rate: float, the points to be paid up-front
    :param var_rate1: float, teaser rate for a two rate mortgage
    :param var_rate2: float, interest rate for a two rate mortgage
    :param var_months: int, amount of mounts for which to pay the teaser rate
    """
    total_months = years * 12
    fixed_mort = Fixed(amount, fixed_rate, total_months)
    fixed_points = FixedWithPoints(amount, points_rate, total_months, points)
    two_rate = TwoRate(amount, var_rate2, total_months, var_rate1,
                       var_months)

    mortgages = [fixed_mort, fixed_points, two_rate]

    # Run experiment
    for m in range(total_months):
        for mort in mortgages:
            mort.make_payment()

    # Report Results
    plot_mortgages(mortgages, amount)


def plot_mortgages(mortgages, amount):
    """ Plots the payments of a set of mortgages
    :param mortgages: list of Mortgages
    :param amount: float, total amount of the loan
    """
    styles = ['b-', 'r-.', 'g:']
    payments = 0
    cost = 1
    pylab.figure(payments)
    pylab.title('Monthly Payments of Different Eu' + str(amount) + ' Mortgages.' )
    pylab.xlabel('Months')
    pylab.ylabel('Monthly Payments')
    pylab.figure(cost)
    pylab.title('Cost of Different Eu' + str(amount) + ' Mortgages.')
    pylab.xlabel('Months')
    pylab.ylabel('Total Payments')

    for i in range(len(mortgages)):
        pylab.figure(payments)
        mortgages[i].plot_payments(styles[i])
        pylab.figure(cost)
        mortgages[i].plot_total_paid(styles[i])

    pylab.figure(payments)
    pylab.legend(loc='upper center')
    pylab.figure(cost)
    pylab.legend(loc='best')


def find_payment(loan, r, m):
    """ Returns the monthly payment for a loan
    :param loan: float, total amount of loan
    :param r: float, monthly interest rate
    :param m: int, number of months
    :return: float, the monthly payment
    """
    return loan * ((r * (1 + r)**m)/((1 + r)**m - 1))


class MortgagePlots(object):
    """ Class used to plot mortgage payments """
    def plot_payments(self, style):
        pylab.plot(self.paid[1:], style, label=self.legend)

    def plot_total_paid(self, style):
        total_paid = [self.paid[0]]
        for i in range(1, len(self.paid)):
            total_paid.append(total_paid[-1] + self.paid[i])
        pylab.plot(total_paid, style, label=self.legend)


class Mortgage(MortgagePlots, object):
    """ Class used to compute mortgage payments """

    def __init__(self, loan, ann_rate, months):
        """ Set up the mortgage
        :param loan: float, initial value of the loan
        :param ann_rate: float, annual interest rate
        :param months: int, number of months to pay the mortgage
        """
        self.loan = loan
        self.rate = ann_rate / 12.0
        self.months = months
        self.paid = [0.0]
        self.owed = [loan]
        self.payment = find_payment(loan, self.rate, months)
        self.legend = None

    def make_payment(self):
        """ Make a single payment on the mortgage """
        self.paid.append(self.payment)
        reduction = self.payment - self.owed[-1] * self.rate
        self.owed.append(self.owed[-1] - reduction)

    def total_paid(self):
        """
        :return: float, total amount paid so far
        """
        return sum(self.paid)

    def __str__(self):
        return self.legend


class Fixed(Mortgage):
    """ Represents a fixed-rate mortgage """
    def __init__(self, loan, rate, months):
        Mortgage.__init__(self, loan, rate, months)
        self.legend = 'Fixed, ' + str(rate * 100) + '%'


class FixedWithPoints(Fixed):
    """ Represents a fixed-rate mortgage with up-front points (payment) """
    def __init__(self, loan, rate, months, points):
        Fixed.__init__(self, loan, rate, months)
        self.points = points
        self.paid = [loan * (points / 100.0)]
        self.legend += ', ' + str(points) + ' points'


class TwoRate(Mortgage):
    """ Represents mortgages that change interest after a set of months """
    def __init__(self, loan, rate, months, teaser_rate, teaser_months):
        Mortgage.__init__(self, loan, teaser_rate, months)
        self.teaser_months = teaser_months
        self.tease_rate = teaser_rate
        self.next_rate = rate / 12.0
        self.legend = str(teaser_rate * 100) \
            + '% for ' + str(self.teaser_months) \
            + ' months, then ' + str(rate * 100) + '%'

    def make_payment(self):
        if len(self.paid) == self.teaser_months + 1:
            self.rate = self.next_rate
            self.payment = find_payment(self.owed[-1], self.rate,
                                        self.months - self.teaser_months)
        Mortgage.make_payment(self)


if __name__ == '__main__':
    #set line width
    pylab.rcParams['lines.linewidth'] = 6
    #set font size for titles
    pylab.rcParams['axes.titlesize'] = 20
    #set font size for labels on axes
    pylab.rcParams['axes.labelsize'] = 20
    #set size of numbers on x-axis
    pylab.rcParams['xtick.major.size'] = 5
    #set size of numbers on y-axis
    pylab.rcParams['ytick.major.size'] = 5

    compare_mortgages(amount=200000, years=30,
                      fixed_rate=0.07,points=3.25,points_rate=0.05,
                      var_rate1=0.045, var_rate2=0.095, var_months=48)

    pylab.show()