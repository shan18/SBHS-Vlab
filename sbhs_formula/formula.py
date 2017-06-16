import random
import math
import os


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
x = os.path.join(BASE_DIR, 'coeff.txt')


class Formula:

    def __init__(self, i):
        self.coeff = []
        with open(x, 'r') as f:
            lines = f.readlines()
        self.coeff = [float(c)+random.uniform(-0.5, 0.5) for c in lines[i].split()]

    def getTemp(self, heat, fan):
        """ Add required Formula here """
        k = self.coeff[0]
        z = self.coeff[1]
        c = self.coeff[2]
        return (k*(1-math.exp(-(heat-fan)/z)))+c

    @staticmethod
    def countCoeff():
        """ This method counts the number of Coefficient Sets available"""
        with open(x,'r') as f:
            lines = f.readlines()
        return len(lines)
