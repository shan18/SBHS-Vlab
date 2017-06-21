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
        self.temp = random.uniform(25.0, 27.0)
        self.formula = Formula(coeff_ID)
        
    def setHeat(self, val):
        """ Set the heat """
        if val > MAX_HEAT or val < 0:
            print 'Error: heat value cannot be more than %d' % MAX_HEAT
            return False

        self.heat = val
        return True

    def setFan(self, val):
        """ Set the fan """
        if val > MAX_FAN or val < 0:
            print 'Error: fan value cannot be more than %d' % MAX_FAN
            return False
        self.fan = val
        return True

    def getTemp(self, instantaneous_time):
        """ Get the temperature """
        return round(self.formula.getTemp(self.heat, self.fan, instantaneous_time) + self.temp, 2)

    def getHeat(self):
        return self.heat

    def getFan(self):
        return self.fan

    def reset_board(self):
        self.setFan(100)
        self.setHeat(0)

    

    def log(self, msg, level):
        try:
            errfile = open(LOG_FILE, 'a') # open error log file in append mode
            if not errfile:
                return
            log_msg = '%s %s %s\n' %(level, strftime('%d:%m:%Y %H:%M:%S', localtime()), msg)
            errfile.write(log_msg)
            errfile.close()
            return
        except:
            return
			

