import random
import math
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
class Formula:
    def __init__(self):
        self.c = 0
        x = os.path.join(BASE_DIR,'coeff.txt')
        with open(x,'r') as f:
            lines = f.readlines()
            i = random.randint(0,len(lines)-1)
            print lines[i]
            self.k,self.z = lines[i].split()
            self.k,self.z = float(self.k),float(self.z)
    def getTemp(self,heat,fan):
        return ((self.k*(1-math.exp(-(heat-fan)/self.z)))+self.c)
