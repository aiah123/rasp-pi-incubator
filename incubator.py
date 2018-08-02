import time
import sys, os
import RPi.GPIO as GPIO
from switch_control import switch_send_signal
import thermometer as thermo


class Incubator:
        def __init__(self, target_temp=40, tolerance=2, measure_interval=10, way_too_high_temp=50):
                self.on_switch = 11
                self.off_switch = 13                
                self.target = target_temp
                self.tol = tolerance
                self.way_too_high_temp = way_too_high_temp
                self.is_heater_on = False
                self.measure_interval = measure_interval
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.on_switch, GPIO.OUT)
                GPIO.setup(self.off_switch, GPIO.OUT)
                                
        def start_incubating(self):
                while True:
                        temperature = thermo.get_temperature()
                        #print(temperature)
                        if temperature > self.way_too_high_temp:
                                raise ValueError('Waaaaay to high temperature: ' + str(self.way_too_high_temp) + '. '
                                                                                                                 'Closing everything')
                        if temperature < self.target - self.tol and not self.is_heater_on:
                               self.start_heating(temperature)
                        elif temperature > self.target + self.tol and self.is_heater_on:
                                self.stop_heating(temperature)
                        elif temperature < self.target - 2*self.tol:
                               print('Must heat')
                               self.start_heating(temperature)
                        elif temperature > self.target + 2*self.tol:
                               print('Must stop heating')
                               self.stop_heating(temperature)
                        else:
                                print("doing nothing ("+ str(temperature) + ")")
                                time.sleep(self.measure_interval)
                        
        def start_heating(self, temperature):
                print("start heating ("+ str(temperature) + ")")
                switch_send_signal(self.on_switch, 1)
                self.is_heater_on = True

        def stop_heating(self, temperature):
                print("stop heating ("+ str(temperature) + ")")
                switch_send_signal(self.off_switch, 1)
                self.is_heater_on = False        


def main():
        try:
             incubator = Incubator(tolerance=0.5, measure_interval=10)
             incubator.start_incubating()
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)
        finally:
                temperature = thermo.get_temperature()
                incubator.stop_heating(temperature)
                switch_send_signal(incubator.off_switch, 1)
                GPIO.cleanup()
                print("See you next time!")


if __name__ == "__main__":
	main()
	
