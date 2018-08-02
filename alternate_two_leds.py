import RPi.GPIO as GPIO
import time

curr_state = True

def alternate_led(pin_num, curr_state):
	if curr_state:
		print "Led On"
		print "curr: %d" % (curr_state)
		GPIO.output(pin_num,GPIO.HIGH)
	        curr_state = False
	else:
	        print "Led off"
		print "curr: %d" % (curr_state)
	        GPIO.output(pin_num,GPIO.LOW)
	        curr_state = True
	return curr_state

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)


while True:
	time.sleep(0.8)
	curr_state = alternate_led(13, curr_state)
	alternate_led(11, curr_state)



