import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

data_pin = 7

GPIO.setup(data_pin, GPIO.IN)
while True:
	print(GPIO.input(data_pin))
	sleep(0.33)
	

'''for data_pin in range(1,40, 1):
	error_found = False	
	try:		
		print('data pin %d:' % (data_pin))
		GPIO.setup(data_pin, GPIO.IN)	
		GPIO.input(data_pin)
		print(GPIO.input(data_pin))
		
	except ValueError:
		error_found = True
		#print ('error with data pin %d' % (data_pin))
		pass
	except TypeError:
		error_found = True
		#print ('not data pin %d' % (data_pin))
		pass
	if not error_found:
		#print ('No error for data_pin %d!!!!!!!!!1' % (data_pin))

'''

