class BoundedList:

    def __init__(self, max_size):
        self.max_size = max_size
        self.bounded_list = []

    def add(self, x):
        print('before ' + str(self.bounded_list))
        if len(self.bounded_list) >= self.max_size:
            self.bounded_list = self.bounded_list[1:]
        self.bounded_list.append(x)
        print('after ' + str(self.bounded_list))

    def __getitem__(self, key):
        return self.bounded_list[key]


    def __str__(self):
        return str(self.bounded_list)

    def size(self):
        return len(self.bounded_list)

#
# my_list = BoundedList(5)
# my_list.add(2)
# my_list.add(3)
# my_list.add(4)
# my_list.add(5)
# my_list.add(7)
# my_list.add(8)
# my_list.add(9)
# my_list.add(10)
# my_list.add(11)
# print(my_list)
# print(my_list[1])
