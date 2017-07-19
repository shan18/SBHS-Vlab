import random
import math
import os

from global_values import GlobalValues

# In constants.txt
""" Columns:
        kp_heat
        tau1_heat
        tau2_heat
        
        kp_fan
        tau1_fan
        tau2_fan
"""
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
x = os.path.join(BASE_DIR, 'constants.txt')


class Formula:

    def __init__(self, i):
        self.coeff = []
        with open(x, 'r') as f:
            lines = f.readlines()
        self.coeff = [float(c) for c in lines[i].split()]

        GlobalValues.kp_heat += self.coeff[0]
        GlobalValues.tau1_heat += self.coeff[1]
        GlobalValues.tau2_heat += self.coeff[2]

        if GlobalValues.tau1_heat == GlobalValues.tau2_heat:
            GlobalValues.tau1_heat += 5

        GlobalValues.kp_fan += self.coeff[3]
        GlobalValues.tau1_fan += self.coeff[4]
        GlobalValues.tau2_fan += self.coeff[5]

        if GlobalValues.tau1_fan == GlobalValues.tau2_fan:
            GlobalValues.tau1_fan += 5

    @staticmethod
    def get_temp(heat, fan):
        """ Add required Formula here """

        # Effect of heat
        if GlobalValues.flag_heat == 1:  # Capturing change in heat input
            GlobalValues.t_store_heat = GlobalValues.instantaneous_time  # Noting down last value of time at heat input change
            GlobalValues.y_offset_heat = GlobalValues.y_heat  # Noting down last value of output at heat input change

        GlobalValues.t_heat = GlobalValues.instantaneous_time - GlobalValues.t_store_heat  # Starting time from zero for heat

        GlobalValues.y_heat = GlobalValues.y_offset_heat + (
            GlobalValues.kp_heat * heat * (
                1 - (
                    GlobalValues.tau1_heat * math.exp(-GlobalValues.t_heat / GlobalValues.tau1_heat) -
                    GlobalValues.tau2_heat * math.exp(-GlobalValues.t_heat / GlobalValues.tau2_heat)
                ) /
                (GlobalValues.tau1_heat - GlobalValues.tau2_heat)
            )
        )

        # Effect of fan
        if GlobalValues.flag_fan == 1:  # Capturing change in fan input
            GlobalValues.t_store_fan = GlobalValues.instantaneous_time  # Noting down last value of time at fan input change
            GlobalValues.y_offset_fan = GlobalValues.y_fan  # Noting down last value of output at fan input change

        GlobalValues.t_fan = GlobalValues.instantaneous_time - GlobalValues.t_store_fan  # Starting time from zero for fan

        GlobalValues.y_fan = GlobalValues.y_offset_fan + (
            GlobalValues.kp_fan * fan * (
                1 - (
                    GlobalValues.tau1_fan * math.exp(-GlobalValues.t_fan / GlobalValues.tau1_fan) -
                    GlobalValues.tau2_fan * math.exp(-GlobalValues.t_fan / GlobalValues.tau2_fan)
                ) /
                (GlobalValues.tau1_fan - GlobalValues.tau2_fan)
            )
        )

        # Combining the effects
        y = GlobalValues.y_heat + GlobalValues.y_fan + GlobalValues.room_temp + random.uniform(-0.3, 0.3)

        if y < GlobalValues.room_temp:
            y = GlobalValues.room_temp
        if y > GlobalValues.max_temp:
            y = GlobalValues.max_temp

        return y

    @staticmethod
    def count_coeff():
        """ This method counts the number of Coefficient Sets available"""
        with open(x, 'r') as f:
            lines = f.readlines()
        return len(lines)
