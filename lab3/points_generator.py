#!/usr/bin/python
import random
import math
from abc import ABCMeta
from abc import abstractmethod
from point import *
from enum import Enum

class FuncType(Enum):
	Parabola = 0
	Line = 1
	Sin = 2


class Func:
	__metaclass__ = ABCMeta

	@abstractmethod
	def set_koef(self, k):
		return None

	@abstractmethod
	def get_koef(self):
		return None

	@abstractmethod
	def get_fx(self, x):
		return None


class Parabola(Func):
	def __init__(self):
		self.parabola = dict()
		koef = dict()
		koef['a'] = 1
		koef['b'] = 1
		koef['c'] = 0

		self.set_koef(koef)

	def set_koef(self, k):
		self.parabola['a'] = k['a']
		self.parabola['b'] = k['b']
		self.parabola['c'] = k['c']

	def get_koef(self):
		return self.parabola

	def get_fx(self, x):
		result =	self.parabola['a'] * x**2 + \
				self.parabola['b'] * x + \
				self.parabola['c']
		return result

class Line(Func):
	def __init__(self):
		self.line = dict()
		koef = dict()
		koef['k'] = 1
		koef['c'] = 0

		self.set_koef(koef)

	def set_koef(self, k):
		self.line['k'] = k['k']
		self.line['c'] = k['c']

	def get_koef(self):
		return self.line

	def get_fx(self, x):
		return self.line['k'] * x + self.line['c']

class Sin(Func):
	def __init__(self):
		self.sin = dict()
		k = dict()
		k['c'] = 0
		k['k'] = 1
		k['kx'] = 1

		self.set_koef(k)

	def set_koef(self, k):
		self.sin['c'] = k['c']
		self.sin['k'] = k['k']
		self.sin['kx'] = k['kx']

	def get_koef(self):
		return self.sin

	def get_fx(self, x):
		return self.sin['k'] * math.sin(self.sin['kx'] * x) + self.sin['c']

class PointGenerator:
	def __init__(self):
		self.cur_function = FuncType.Parabola

	def get_default_2D(self):
		#points = [(0, 0), (1, 0), (0, 1), (1, 1)]
		#points = [(1, 2), (1, -1), (0, 1), (1, 0), (0, 0), (1, 1)]
		points = [ (2, 7, 0), (2, 6, 0), (3, 5, 0), (2, 3, 0), \
				(3, 1, 0), (5, 6, 0), (6, 5, 0), (7, 5, 0), \
				(7, 4, 0)]
		points = list(map(Point,points))
		return points

	def get_default_3D(self):
		points = [(0,0,0), (1,2,3), (0,5,7), (5, 0, 4)]
		points = list(map(Point, points))
		return points

	def enable_parabola(self, a, b, c):
		self.cur_function = FuncType.Parabola

		k = dict()
		k['a'] = a
		k['b'] = b
		k['c'] = c

		self.func = Parabola()
		self.func.set_koef(k)

	def enable_line(self, kx, c):
		self.cur_function = FuncType.Line

		k = dict()
		k['k'] = kx
		k['c'] = c

		self.func = Line()
		self.func.set_koef(k)

	def enable_sin(self, k, kx, c):
		self.cur_function = FuncType.Sin

		koef = dict()
		koef['k'] = k
		koef['kx'] = kx
		koef['c'] = c

		self.func = Sin()
		self.func.set_koef(koef)

	def __get_two_func__(self, delta):
		func1 = None
		func2 = None

		if self.cur_function == FuncType.Parabola:
				func1 = Parabola()
				func2 = Parabola()
		if self.cur_function == FuncType.Sin:
				func1 = Sin()
				func2 = Sin()
		if self.cur_function == FuncType.Line:
				func1 = Line()
				func2 = Line()

		koef = self.func.get_koef()
		k = dict()
		for (key, v) in koef.items():
			k[key] = v

		k['c'] = k['c'] + delta
		func1.set_koef(k)

		k['c'] = k['c'] - delta * 2
		func2.set_koef(k)

		return [func1, func2]

	def __get_normal_prob_val__(self):
		x1_low = -2
		x1_up = 2
		x = random.random() * (x1_up - x1_low) + x1_low

		mu = 0
		sigma_2 = 1
		p = 0.5 * (1 + math.erf((x - mu) / math.sqrt(2 * sigma_2)))
		return p

	def generate_points(self, x1, x2, z0, R):
		x_step = 0.4
		z_step = 0.4
		n_max = 7
		points = []

		z = z0 - R + z_step
		while z < (z0 + R):
			delta = math.sqrt(R ** 2 - (z - z0)**2)

			func_arr = self.__get_two_func__(delta)
			func1 = func_arr[0]
			func2 = func_arr[1]

			x = x1
			while x <= x2:
				y1 = func1.get_fx(x)
				y2 = func2.get_fx(x)
				n_cur = int(n_max * self.__get_normal_prob_val__())

				for n in range(n_cur):
					prob_y = self.__get_normal_prob_val__()
					prob_z = self.__get_normal_prob_val__()
					new_point = (x, float(y2) + prob_y * (y1 - y2), float(z) + z_step * prob_z)
					points.append(new_point)

				x = x + x_step
			z = z + z_step

		points = list(map(Point,points))
		return points
