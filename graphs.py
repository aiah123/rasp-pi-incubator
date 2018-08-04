import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

TEMP_INDEX = 0
DATE_INDEX = 1
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

start_time = '2018-08-02 22:00:01.696912'
end_time = '2018-08-03 20:38:01.696912'

fname = 'temp.log'
with open(fname) as file:
    lines = [line.strip() for line in file]


data = np.array([[x.split(maxsplit=1)[TEMP_INDEX][:-1], x.split(maxsplit=1)[1]] for x in lines])
temps = data[:,0]
dates = np.array([datetime.strptime(x, TIMESTAMP_FORMAT) for x in data[:,1]])

formatted_start_date = datetime.strptime(end_time, TIMESTAMP_FORMAT)
formatter_end_date = datetime.strptime(start_time, TIMESTAMP_FORMAT)
dates_in_range = (dates < formatted_start_date) & (dates >= formatter_end_date)

temps = temps[dates_in_range]
dates = dates[dates_in_range]

plt.plot(dates, temps, '.-')
plt.axhline(40.15)
plt.axhline(39.85, c="r")
plt.show()

