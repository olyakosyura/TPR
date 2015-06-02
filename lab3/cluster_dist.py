#!/usr/bin/python

from enum import Enum
from abc import abstractmethod

class DistType(Enum):
		FarNeighbor = 0
		Uord = 1
		Center = 2
		NearNeighbor = 3
		Middle = 4

class DistBase:
		@abstractmethod
		def get_a_u(self, u, v, w, s):
				return 0
		@abstractmethod
		def get_a_v(self, u, v, w, s):
				return 0
		@abstractmethod
		def get_b(self, u, v, w, s):
				return 0
		@abstractmethod
		def get_g(self, u, v, w, s):
				return 0

class FarNeighbor(DistBase):
		def __init__(self):
				self.alpha_u = 0.5
				self.alpha_v = 0.5
				self.betta = 0
				self.gamma = 0.5

		def get_a_u(self, u, v, w, s):
				return self.alpha_u
		def get_a_v(self, u, v, w, s):
				return self.alpha_v
		def get_b(self, u, v, w, s):
				return self.betta
		def get_g(self, u, v, w, s):
				return self.gamma

class NearNeighbor(DistBase):
		def __init__(self):
				self.alpha_u = 0.5
				self.alpha_v = 0.5
				self.betta = 0
				self.gamma = -0.5

		def get_a_u(self, u, v, w, s):
				return self.alpha_u
		def get_a_v(self, u, v, w, s):
				return self.alpha_v
		def get_b(self, u, v, w, s):
				return self.betta
		def get_g(self, u, v, w, s):
				return self.gamma

class Uord(DistBase):
		def get_a_u(self, u, v, w, s):
				return float((s + u)) / (s + w)
		def get_a_v(self, u, v, w, s):
				return float(s + v) / (s + w)
		def get_b(self, u, v, w, s):
				return -float(s) / (s + w)
		def get_g(self, u, v, w, s):
				return 0

class Center(DistBase):
		def get_a_u(self, u, v, w, s):
				return float(u) / (w)
		def get_a_v(self, u, v, w, s):
				return float(v) / (w)
		def get_b(self, u, v, w, s):
				return - float(u * v) / (w * w)
		def get_g(self, u, v, w, s):
				return 0

class Middle(DistBase):
		def get_a_u(self, u, v, w, s):
				return float(u) / (w)
		def get_a_v(self, u, v, w, s):
				return float(v) / (w)
		def get_b(self, u, v, w, s):
				return 0
		def get_g(self, u, v, w, s):
				return 0

