from time import localtime
from time import strftime

import sys
import os
import random

# The following line is needed to import Formula
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from sbhs_formula.formula import Formula
from sbhs_formula.formula import Formula

# LOG_FILE = '../log/sbhserr.log'
LOG_FILE = '/tmp/sbhserr.log'

MAX_HEAT = 100
MAX_FAN = 100


class Sbhs:
    """ This is the Single Board Heater System class """

    """ self.temp signifies the previous temperature measurement.It is intially set randomly"""
    def __init__(self, coeff_ID):
        # status of the board
        self.status = 0
        self.heat = 0
        self.fan = 0
        self.formula = Formula(coeff_ID)
        
    def set_heat(self, val):
        """ Set the heat """
        if val > MAX_HEAT or val < 0:
            print 'Error: heat value cannot be more than %d' % MAX_HEAT
            return False

        self.heat = val
        return True

    def set_fan(self, val):
        """ Set the fan """
        if val > MAX_FAN or val < 0:
            print 'Error: fan value cannot be more than %d' % MAX_FAN
            return False
        self.fan = val
        return True

    def get_temp(self, instantaneous_time, room_temp):
        """ Get the temperature """
        return round(self.formula.get_temp(self.heat, self.fan, instantaneous_time) + room_temp, 2)

    def get_heat(self):
        return self.heat

    def get_fan(self):
        return self.fan

    def reset_board(self):
        self.set_fan(100)
        self.set_heat(0)

    def log(self, msg, level):
        try:
            err_file = open(LOG_FILE, 'a') # open error log file in append mode
            if not err_file:
                return
            log_msg = '%s %s %s\n' %(level, strftime('%d:%m:%Y %H:%M:%S', localtime()), msg)
            err_file.write(log_msg)
            err_file.close()
            return
        except:
            return
