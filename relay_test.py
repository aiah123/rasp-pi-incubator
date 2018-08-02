import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

def on_off_loop():
	while (True):
		print('High')
		GPIO.output(11,GPIO.HIGH)
		time.sleep(1)
		print('Low')
		GPIO.output(11,GPIO.LOW)
		time.sleep(1)

if __name__=="__main__":
    on_off_loop()
