__author__ = 'nunoe'


class Field(object):

    def __init__(self):
        self.drunks = {}

    def add_drunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate Drunk.')
        else:
            self.drunks[drunk] = loc

    def move_drunk(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in Field.')
        x_dist, y_dist = drunk.take_step()
        current_location = self.drunks[drunk]
        self.drunks[drunk] = current_location.move_to(x_dist, y_dist)

    def get_loc(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in Field.')
        return self.drunks[drunk]