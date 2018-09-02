import RPi.GPIO as GPIO
import time

current_state = GPIO.HIGH

while True:
	time.sleep(1)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)
	
	if current_state == GPIO.LOW:
		print "Led On"
		GPIO.output(7,GPIO.HIGH)
		current_state = GPIO.HIGH
	else:
		print "Led off"
		GPIO.output(7,GPIO.LOW)
		current_state = GPIO.LOW

