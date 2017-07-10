import random
import math
import os


# In constants.txt
# First column: K
# Second column: tow
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
x = os.path.join(BASE_DIR, 'constants.txt')


class Formula:

    def __init__(self, i):
        self.coeff = []
        with open(x, 'r') as f:
            lines = f.readlines()
        self.coeff = [float(c) for c in lines[i].split()]

    def get_temp(self, heat, fan, instantaneous_time):
        """ Add required Formula here """
        k = self.coeff[0]

        """ 2nd Order Model  (Update the constants.txt file accordingly)
        tow_1 = self.coeff[1]
        tow_2 = self.coeff[2]
        exp_power_1 = -1 * (instantaneous_time / tow_1)
        exp_power_2 = -1 * (instantaneous_time / tow_2)
        val = (tow_1 * math.exp(exp_power_1) - tow_2 * math.exp(exp_power_2)) / (tow_1 - tow_2)
        heat_value = k * heat * (1 - val)
        return heat_value + random.uniform(-0.5, 0.5)
        """

        # 1st Order Model
        tow = self.coeff[1]

        # Effect of Heat
        exp_power = -1 * (instantaneous_time / tow)
        value = k * (1 - math.exp(exp_power))
        change_in_output_for_heat = value * heat

        # Effect of Fan
        change_in_output_for_fan = fan

        change_in_output = abs(change_in_output_for_heat - change_in_output_for_fan)
        return change_in_output + random.uniform(-0.5, 0.5)

    @staticmethod
    def count_coeff():
        """ This method counts the number of Coefficient Sets available"""
        with open(x, 'r') as f:
            lines = f.readlines()
        return len(lines)
