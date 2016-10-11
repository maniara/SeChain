class Contract(object):
    """docstring for """
    def __init__(self,a,b):
        self.a = '10'
        self.b = a
    def add(self,arg):
        self.a += arg
        return self.a
