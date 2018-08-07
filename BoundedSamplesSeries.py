class BoundedSamplesSeries:

    def __init__(self, max_size):
        self.max_size = max_size
        self.bounded_list = []

    def add(self, x):
        if len(self.bounded_list) >= self.max_size:
            self.bounded_list = self.bounded_list[1:]
        self.bounded_list.append(x)

    def __getitem__(self, key):
        return self.bounded_list[key]

    def __str__(self):
        return str(self.bounded_list)

    def size(self):
        return len(self.bounded_list)

    # returns true if the temperature is a monotonically increasing series
    def temperature_increasing(self):
        if not self.has_enough_samples():
            return False
        return self.is_series_by_f(lambda x, y: x > y)

    # returns true if the temperature is a monotonically decreasing series
    def temperature_decreasing(self):
        if not self.has_enough_samples():
            return False
        return self.is_series_by_f(lambda x, y: x < y)

    def has_enough_samples(self):
        if self.size() < self.max_size:
            return False
        return True

    # f is a boolean lambda function that takes two consecutive elements in the series (e.g, larger than)
    # The method returns true if the series does NOT apply for comply with f.
    # E.g, the lambda  (lambda x, y: x < y)
    # will return true if the series is monotonically decreasing.
    def is_series_by_f(self, f):
        for sample_index in range(self.size() - 1):
            curr_sample = self.bounded_list[sample_index]
            next_sample = self.bounded_list[sample_index + 1]
            if f(curr_sample, next_sample):
                return False

        return True


#
my_list = BoundedSamplesSeries(5)
my_list.add(3)
my_list.add(3)
my_list.add(4)
my_list.add(5)
my_list.add(5)
my_list.add(8)
my_list.add(9)
my_list.add(10)
my_list.add(11)
my_list.add(12)
print(my_list)
print(my_list.temperature_increasing())
print(my_list.temperature_decreasing())
