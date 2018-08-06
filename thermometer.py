import time
import datetime



temp_log_file_name = "src/temp.log"
temperature_source_file = "/sys/bus/w1/devices/28-0517a02b5dff/w1_slave"


def get_temperature():
	temperature = get_temperature_from_file(temperature_source_file)
	write_temp_to_file(temperature, temp_log_file_name)
	return temperature

def get_temperature_from_file(temprature_source_file):
    with open(temprature_source_file,"r") as f:
        f_text = f.read()
    temperature = eval(f_text.split("t=")[1]) / 1000.
    return temperature

def write_temp_to_file(temperature, file_name):
    with open(file_name,"a") as f:
        line = str(temperature) + "C\t     " + str(datetime.datetime.now()) + "\n"
        f.write(line)

def measure_temp_sequence(interval):    
    while True:
        temperature = get_temperature_from_file(temperature_source_file)
        #print(str(temperature) + " C")
        write_temp_to_file(temperature, temp_log_file_name)
        time.sleep(interval)


if __name__ == "__main__":
	measure_temp_sequence(10)
	#temperature = parse_temperature(f_text)
	#print(temperature)
