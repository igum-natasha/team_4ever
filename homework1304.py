from math import sqrt
class Calculate:
    def __init__(self):
        self.result=None
        self.base_of_data=[]
    def add(self,a,b):
        self.result=a+b
    def subst(self,a,b):
        self.result=a-b
    def mult(self,a,b):
        self.result=a*b
    def div(self,a,b):
        self.result=a/b
    def mod(self,a,b):
        self.result = a % b
    def sqrt_of_num(self,a):
        self.result = sqrt(a)
    def create_base_of_data(self):
        self.base_of_data.append(self.result)
