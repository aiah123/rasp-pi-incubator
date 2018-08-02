import RPi.GPIO as GPIO
import time

def switch_send_signal(gpio_num, interval):
	
	GPIO.output(gpio_num, GPIO.HIGH)
	time.sleep(interval)
	GPIO.output(gpio_num, GPIO.LOW)

