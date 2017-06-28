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
        # coeff.txt has values in format: mass  resistance  specific heat
        self.coeff = [float(c) for c in lines[i].split()]

    def getTemp(self, heat, fan, instantaneous_time):
        """ Add required Formula here """
        mass = self.coeff[0]
        resistance = self.coeff[1]
        sp_heat = self.coeff[2]
        current = heat / 50
        heat_in_joules = pow(current, 2) * resistance
        return heat_in_joules / (mass * sp_heat)

    @staticmethod
    def countCoeff():
        """ This method counts the number of Coefficient Sets available"""
        with open(x,'r') as f:
            lines = f.readlines()
        return len(lines)
