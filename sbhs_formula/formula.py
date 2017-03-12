import random
import math
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
class Formula:
    def __init__(self):
        x = os.path.join(BASE_DIR,'coeff.txt')
        with open(x,'r') as f:
            lines = f.readlines()
            self.i = random.randint(0,len(lines)-1)
            self.k,self.z,self.c = lines[self.i].split()
            self.k,self.z,self.c = float(self.k),float(self.z),float(self.c)
    def getTemp(self,heat,fan):
        """ Add required Formula here """
        return ((self.k*(1-math.exp(-(heat-fan)/self.z)))+self.c)
