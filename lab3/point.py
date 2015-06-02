#!/usr/bin/python
import math

class Point:
		def __init__(self, point):
				self.p = point

		def set(self, point):
				self.p = point

		def dist(self, point):
				if len(self.p) != len(point.p):
						print("ERR: unable to get dist between different dimention points")
						return -1

				dist = 0
				for i in range(len(self.p)):
						dist += (self.p[i] - point.p[i]) ** 2

				return math.sqrt(dist)

		def __str__(self):
				string = "({}".format(self.p[0])

				for i in range(1, len(self.p)):
						cur_coordinate = ", {}".format(self.p[i])
						string = string + cur_coordinate
				string = string + ")"
				return string

		def __repr__(self):
				return self.__str__()
