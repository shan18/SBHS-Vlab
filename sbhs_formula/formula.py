import random
import math
import os


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
x = os.path.join(BASE_DIR, 'coeff_2nd_order.txt')


class Formula:

    def __init__(self, i):
        self.coeff = []
        with open(x, 'r') as f:
            lines = f.readlines()
        self.coeff = [float(c) for c in lines[i].split()]

    def getTemp(self, heat, fan, instantaneous_time):
        """ Add required Formula here """
        k = self.coeff[0]

        """ 1st Order Model
        tow = self.coeff[1]
        exp_power = -1 * (instantaneous_time / tow)
        value = k * (1 - math.exp(exp_power))
        heat_value = (value * heat) + random.uniform(-0.5, 0.5)
        """

        # 2nd Order Model
        tow_1 = self.coeff[1]
        tow_2 = self.coeff[2]
        exp_power_1 = -1 * (instantaneous_time / tow_1)
        exp_power_2 = -1 * (instantaneous_time / tow_2)
        val = (tow_1 * math.exp(exp_power_1) - tow_2 * math.exp(exp_power_2)) / (tow_1 - tow_2)
        heat_value = k * heat * (1 - val)
        return heat_value + random.uniform(-0.5, 0.5)

    @staticmethod
    def countCoeff():
        """ This method counts the number of Coefficient Sets available"""
        with open(x,'r') as f:
            lines = f.readlines()
        return len(lines)
