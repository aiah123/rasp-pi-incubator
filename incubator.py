import getopt, sys
import time
import datetime
import sys, os
import RPi.GPIO as GPIO
from .switch_control import switch_send_signal
from .thermometer import get_temperature
from .BoundedSamplesSeries import *
import numpy as np

log_file_name = 'rasp-pi-incubator/logs/incubator_log.log'
MIN_LAST_SAMPLES_KEPT = 4
DEFAULT_TOLERANCE = 0.1
DEFAULT_TARGET_TEMERATURE = 33

class Incubator:
    def __init__(self, target_temp=36, tolerance=2., measure_interval=10, way_too_high_temp=50,
                 tolerance_multiplier=2):
        self.on_switch = 16
        self.off_switch = 18
        self.target = target_temp
        self.tol = tolerance
        self.way_too_high_temp = way_too_high_temp
        self.is_heater_on = False
        self.measure_interval = measure_interval
        self.tolerance_multiplier = tolerance_multiplier

        # the list should keep samples from the last 30 seconds (or at least 5 last samples)
        self.last_samples_list = BoundedSamplesSeries(max(MIN_LAST_SAMPLES_KEPT, 30.0 / self.measure_interval))
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.on_switch, GPIO.OUT)
        GPIO.setup(self.off_switch, GPIO.OUT)

    def start_incubating(self):
        while True:
            temperature = get_temperature()
            self.last_samples_list.add(temperature)
            if temperature > self.way_too_high_temp:
                raise ValueError('Waaaaay to high temperature: ' + str(self.way_too_high_temp) + '. '
                                                                                             'Closing everything')
            if temperature < self.target - self.tol and not self.is_heater_on:
                self.start_heating(temperature)
            elif temperature > self.target + self.tol and self.is_heater_on:
                self.stop_heating(temperature)
            elif temperature < self.target - self.tolerance_multiplier * self.tol and self.last_samples_list.temperature_decreasing():
                self.log('Must heat')
                self.start_heating(temperature)
            elif temperature > self.target + self.tolerance_multiplier * self.tol and self.last_samples_list.temperature_increasing():
                self.log('Must stop heating')
                self.stop_heating(temperature)
            else:                
                print("doing nothing (" + str(temperature) + ")")

            time.sleep(self.measure_interval)

    def start_heating(self, temperature):
        self.log("start heating (" + str(temperature) + ")")
        switch_send_signal(self.on_switch, 1)
        self.is_heater_on = True

    def stop_heating(self, temperature):
        self.log("stop heating (" + str(temperature) + ")")
        switch_send_signal(self.off_switch, 1)
        self.is_heater_on = False


    @staticmethod
    def log(log_str):
        log_str = str(datetime.datetime.now()) + ' ' + log_str
        with open(log_file_name, "aw+") as f:
            print(log_str)
            line = str(log_str) + "\n"
            f.write(line)


def main(argv):
    try:

        target_temp, tolerance = get_target_temp_and_tolerance(argv)
        incubator = Incubator(tolerance=tolerance, target_temp=target_temp, measure_interval=90)     
        incubator.start_incubating()
    except Exception as e:
        handle_exception(e)
    finally:
        temperature = get_temperature()
        incubator.stop_heating(temperature)  # just in case
        time.sleep(2)
        incubator.stop_heating(temperature)  # second just in case
        switch_send_signal(incubator.off_switch, 1)
        GPIO.cleanup()
        time.sleep(1)
        GPIO.cleanup()
        incubator.log("See you next time!")


def handle_exception(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Incubator.log('%s %s %d' % (exc_type, fname, exc_tb.tb_lineno))
    Incubator.log(str(e))


def get_target_temp_and_tolerance(argv):
    tolerance = DEFAULT_TOLERANCE
    target_temp = DEFAULT_TARGET_TEMERATURE
    opts, args = getopt.getopt(argv, "tar:tol:", ["target_temp=", "tolerance="])
    for opt, arg in opts:
        print(opt, arg)
        if opt in ('-tar', '--target_temp'):
            target_temp = np.float(arg)
        elif opt in ('tol', '--tolerance'):
            tolerance = np.float(arg)

    print('Using target temperature %f and tolerance %f' % (target_temp, tolerance)) 
    return target_temp, tolerance


if __name__ == "__main__":
    main(sys.argv[1:])
