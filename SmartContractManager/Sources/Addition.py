class Contract(object):
    """docstring for """
    def __init__(self,a):
        self.a = a
    def add(self,arg):
        self.a += arg
        return self.a
