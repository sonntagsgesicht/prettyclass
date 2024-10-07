
from prettyclass import prettyclass


@prettyclass()
class ABC:
    def __init__(self, a, *b, c, d=4, e, **f):
        ...
