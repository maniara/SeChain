class Contract(object):
    """docstring for """
    def __init__(self,a):
        self.a = int(a)
    def add(self,arg):
        self.a += int(arg)
        return self.a
