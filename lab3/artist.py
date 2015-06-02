#!/usr/bin/python

from point import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

class Artist3D:
		def __init__(self):
				self.fig = plt.figure()
				self.ax = self.fig.gca(projection='3d')

		def draw_points(self, points):
				for p in points:
						self.ax.scatter(p.p[0], p.p[1], p.p[2])

		def draw_cluster_points(self, clusters):
				colors = ["orange", "black", "red", "yellow", "blue", "green"]

				for c in clusters:
						color = colors.pop()
						for p in c:
								self.ax.scatter(p.p[0], p.p[1], p.p[2], c=color)

		def show(self):
				plt.show()
