import time
import datetime
import sys, os
import RPi.GPIO as GPIO
from .switch_control import switch_send_signal
from .thermometer import get_temperature
from .BoundedList import *

log_file_name = 'src/incubator_log.log'
MIN_LAST_SAMPLES_KEPT = 8


class Incubator:
    def __init__(self, target_temp=36, tolerance=2., measure_interval=10, way_too_high_temp=50):
        self.on_switch = 11
        self.off_switch = 13
        self.target = target_temp
        self.tol = tolerance
        self.way_too_high_temp = way_too_high_temp
        self.is_heater_on = False
        self.measure_interval = measure_interval

        # the queue should keep samples from the last 30 seconds (or at least 5 last samples)
        self.last_samples_queue = BoundedList(max(MIN_LAST_SAMPLES_KEPT, 30.0 / self.measure_interval))
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.on_switch, GPIO.OUT)
        GPIO.setup(self.off_switch, GPIO.OUT)

    # returns true if the temperature is a monotonically increasing series
    def temperature_increasing(self):
        if not self.has_enough_samples():
            return False
        print('Is inc' + str(self.last_samples_queue))
        return self.is_series_by_f(lambda x, y: x > y)

    # returns true if the temperature is a monotonically decreasing series
    def temperature_decreasing(self):
        if not self.has_enough_samples():
            return False
        print('Is dec' + str(self.last_samples_queue))
        return self.is_series_by_f(lambda x, y: x < y)

    # f is a boolean lambda function that takes two consecutive elements in the series (e.g, larger than)
    # The method returns true if the series does NOT apply for comply with f.
    # E.g, the lambda  (lambda x, y: x < y)
    # will return true if the series is monotonically decreasing.
    def is_series_by_f(self, f):
        for sample_index in range(self.last_samples_queue.size() - 1):
            curr_sample = self.last_samples_queue[sample_index]
            next_sample = self.last_samples_queue[sample_index + 1]
            print(str(curr_sample) + ' ' + str(next_sample))
            if f(curr_sample, next_sample):
                print('x < y')
                return False
        
        return True

    
    def start_incubating(self):
        while True:
            temperature = get_temperature()
            print(self.target + 2 * self.tol)
            print(self.temperature_increasing())
            print(temperature > self.target + 2 * self.tol)
            if temperature > self.way_too_high_temp:
                raise ValueError('Waaaaay to high temperature: ' + str(self.way_too_high_temp) + '. '
                                                                                                 'Closing everything')
            if temperature < self.target - self.tol and not self.is_heater_on:
                self.start_heating(temperature)
            elif temperature > self.target + self.tol and self.is_heater_on:
                self.stop_heating(temperature)
            elif temperature < self.target - 2 * self.tol and self.temperature_decreasing():
                self.log('Must heat')
                self.start_heating(temperature)
            elif temperature > self.target + 2 * self.tol and self.temperature_increasing():
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

    def has_enough_samples(self):
        if self.last_samples_queue.size() < MIN_LAST_SAMPLES_KEPT:
            return False
        return True

    @staticmethod
    def log(log_str):
        log_str = str(datetime.datetime.now()) + ' ' + log_str
        with open(log_file_name, "a") as f:
            print(log_str)
            line = str(log_str) + "\n"
            f.write(line)


def main():
    try:
        incubator = Incubator(tolerance=0.1, target_temp=33, measure_interval=10)
        incubator.start_incubating()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        incubator.log('%s %s %d' % (exc_type, fname, exc_tb.tb_lineno))
        incubator.log(str(e))
    finally:
        temperature = get_temperature()
        incubator.stop_heating(temperature)  # just in case
        time.sleep(2)
        incubator.stop_heating(temperature)  # second just in case
        switch_send_signal(incubator.off_switch, 1)
        GPIO.cleanup()
        incubator.log("See you next time!")


if __name__ == "__main__":
    main()
