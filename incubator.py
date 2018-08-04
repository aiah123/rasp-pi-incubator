import time
import sys, os
import RPi.GPIO as GPIO
from .switch_control import switch_send_signal
from .thermometer import get_temperature
from .BoundedList import *

log_file_name = 'incubator_log.log'


class Incubator:
    def __init__(self, target_temp=40, tolerance=2., measure_interval=10, way_too_high_temp=50):
        self.on_switch = 11
        self.off_switch = 13
        self.target = target_temp
        self.tol = tolerance
        self.way_too_high_temp = way_too_high_temp
        self.is_heater_on = False
        self.measure_interval = measure_interval
        self.last_samples_queue = BoundedList(max(5, 30.0 / self.measure_interval))
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.on_switch, GPIO.OUT)
        GPIO.setup(self.off_switch, GPIO.OUT)

    # returns true if the temperature is a monotonically increasing series
    def temperature_increasing(self):
        return self.is_series_by_f(lambda x, y: x > y)

    # returns true if the temperature is a monotonically decreasing series
    def temperature_decreasing(self):
        return self.is_series_by_f(lambda x, y: x < y)

    def is_series_by_f(self, f):
        for sample_index in range(self.last_samples_queue.size() - 1):
            curr_sample = self.last_samples_queue[sample_index]
            next_sample = self.last_samples_queue[sample_index + 1]
            if f(curr_sample, next_sample):
                return False
        return True

    def start_incubating(self):
        while True:
            temperature = get_temperature()
            # print(temperature)
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

    @staticmethod
    def log(log_str):
        with open(log_file_name, "a") as f:
            print(log_str)
            line = log_str + "\n"
            f.write(line)


def main():
    try:
        incubator = Incubator(tolerance=0.5, measure_interval=10)
        incubator.start_incubating()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        incubator.log(exc_type, fname, exc_tb.tb_lineno)
        incubator.log(e)
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
