__author__ = 'nunoe'


class Location(object):

    def __init__(self, x, y):
        """
        :param x: float, horizontal coordinate
        :param y: float, vertical coordinate
        """
        self.x = x
        self.y = y

    def move_to(self, delta_x, delta_y):
        """
        :param delta_x: float, distance to move along the x-axis
        :param delta_y: float, distance to move along the y-axis
        :return: Location, the new location after moving
        """
        return Location(self.x + delta_x, self.y + delta_y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def dist_from(self, other):
        """
        :param other: Location, the other location against which to calculate the current point's distance
        :return: float, the distance from self to other
        """
        x_dist = self.x - other.get_x()
        y_dist = self.y - other.get_y()
        return (x_dist ** 2 + y_dist ** 2) ** 0.5

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'