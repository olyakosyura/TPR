#!/usr/bin/python
import sys
from optparse import OptionParser
import math
from point import *
from points_generator import *
from artist import *
from cluster_dist import *

class Cluster:
		def __init__(self, points, dist_type):
				self.points = points
				self.dist_type = dist_type

		def __str__(self):
				if len(self.points) == 0:
						return "empty"

				print_str = ""
				for p in self.points:
						if print_str == "":
								print_str += "[" + str(p)
						else:
								print_str += "; " + str(p)
				print_str += "]"
				return print_str

		def dist(self, cluster):
				# remove this from clusters . use dist between points instead
				if (self.dist_type == DistType.FarNeighbor or \
						self.dist_type == DistType.NearNeighbor or \
						self.dist_type == DistType.Center or \
						self.dist_type == DistType.Middle or \
						self.dist_type == DistType.Uord):
						dist_max = 0
						for p1 in self.points:
								for p2 in cluster.points:
										cur_dist = p1.dist(p2)
										if cur_dist > dist_max:
												dist_max = cur_dist
						return dist_max

				print("ERR: incorrect dist type")
				return -1

class Classificator:
		def __init__(self, set_type):
				self.mode = set_type

				if set_type == DistType.FarNeighbor:
						self.dist_manager = FarNeighbor()

				if set_type == DistType.NearNeighbor:
						self.dist_manager = NearNeighbor()

				if set_type == DistType.Uord:
						self.dist_manager = Uord()

				if set_type == DistType.Center:
						self.dist_manager = Center()

				if set_type == DistType.Middle:
						self.dist_manager = Middle()

				if self.dist_manager is None:
						self.dist_manager = NearNeighbor()
				self.clusters = []

		def __hierarchy_prepare_dist(self):
				clusters_cnt = len(self.clusters)
				dist = [[0 for j in range(i + 1, clusters_cnt)] for i in range(clusters_cnt - 1)]

				for i in range(clusters_cnt - 1):
						for j in range(clusters_cnt - i - 1):
								k = j + i + 1
								dist[i][j] = self.clusters[i].dist(self.clusters[k])

				self.dist = dist

		def __hierarchy_cluster_one_dist(self, R_US, R_VS, R_UV, perform):
				u = perform[0]
				v = perform[1]
				w = u + v
				s = perform[2]
				return self.dist_manager.get_a_u(u, v, w, s) * R_US +	\
						self.dist_manager.get_a_v(u, v, w, s) * R_VS +	\
						self.dist_manager.get_b(u, v, w, s) * R_UV +	\
						self.dist_manager.get_g(u, v, w, s) * math.fabs(R_US - R_VS)

		def __hierarchy_cluster_dist(self, U_index, V_index, S_index, perform):
				if U_index < S_index:
						R_US = self.dist[U_index][S_index - U_index - 1]
				else:
						R_US = self.dist[S_index][U_index - S_index - 1]

				if V_index < S_index:
						R_VS = self.dist[V_index][S_index - V_index - 1]
				else:
						R_VS = self.dist[S_index][V_index - S_index - 1]

				if U_index < V_index:
						R_UV = self.dist[U_index][V_index - U_index - 1]
				else:
						R_UV = self.dist[V_index][U_index - V_index - 1]

				return self.__hierarchy_cluster_one_dist(R_US, R_VS, R_UV, perform)

		def __hierarchy_clusterize(self):
				min_dist = self.dist[0][0]
				min_i = min_j = 0

				for i in range(len(self.dist)):
						for j in range(len(self.dist[i])):
								if self.dist[i][j] < min_dist:
										min_i = i
										min_j = j
										min_dist = self.dist[i][j]

				# indexes of clusters now
				u = min_i
				v = min_j + min_i + 1
				new_column = []
				for i in range(len(self.clusters)):
						if i == v or i == u:
								continue

						perform = [		len(self.clusters[u].points), \
										len(self.clusters[v].points), \
										len(self.clusters[i].points)]
						cur_dist = self.__hierarchy_cluster_dist(u, v, i, perform)
						new_column.append(cur_dist)

				new_dist = []
				k = 0
				for i in range(len(self.dist)):
						if i == u or i == v:
								continue
						new_row = []
						for j in range(len(self.dist[i])):
								if j == (v - i - 1) or j == (u - i - 1):
										continue
								new_row.append(self.dist[i][j])

						new_row.append(new_column[k])
						k += 1
						new_dist.append(new_row)

				if k < len(new_column):
						new_dist.append([new_column[k]])
				self.dist = new_dist

				new_cluster = Cluster(self.clusters[u].points + self.clusters[v].points, self.mode)

				u_cluster = self.clusters[u]
				v_cluster = self.clusters[v]
				self.clusters.remove(u_cluster)
				self.clusters.remove(v_cluster)
				self.clusters.append(new_cluster)

				#print("New clusters:")
				#for c in self.clusters:
				#		print("\t{}".format(c))

		def hierarchy(self, points, class_number):
				for p in points:
						self.clusters.append(Cluster([p], self.mode))

				self.__hierarchy_prepare_dist()

				while (len(self.clusters) > class_number):
						self.__hierarchy_clusterize()

def draw_cluster_points(points):
		art = Artist3D()
		art.draw_cluster_points(points)
		art.show()

def parse_options():
	import sys
	if len(sys.argv) != 3:
		return None

	opt = {}
	opt['cluster_cnt'] = int(sys.argv[1])
	type_dist_map = {
		'single_linkage': DistType.NearNeighbor,
		'ward': DistType.Uord,
		'centroid': DistType.Center,
		'complete_linkage': DistType.FarNeighbor,
		'average': DistType.Middle,
	}
	opt['type_dist'] = type_dist_map[sys.argv[2]]
	return opt

def count_measures(source_points, result_p_clusters):
		cluster_cnt = len(result_p_clusters)
		if cluster_cnt != len(source_points):
				print("ERR: clusters cnt (source and result) mismatch")
				return None

		precisious = [0 for c in range(cluster_cnt)]
		recall = [0 for c in range(cluster_cnt)]
		f1_measure = [0 for c in range(cluster_cnt)]

		cluster_index = 0
		for s_c in source_points:
				cluster_detection = [0 for c in range(cluster_cnt)]
				for s_p in s_c:
						index = 0
						found = 0
						for r_c in result_p_clusters:
								for r_p in r_c:
										if s_p == r_p:
												cluster_detection[index] += 1
												found = 1
												break
								if found == 1:
										break
								index += 1
				max_index = 0
				index = 0
				for cl in cluster_detection:
						if cl > cluster_detection[max_index]:
								max_index = index

						index += 1

				#print("Cluster detection {}".format(cluster_detection))
				precisious[cluster_index] = float(cluster_detection[max_index]) / len(result_p_clusters[max_index])
				recall[cluster_index] = float(cluster_detection[max_index]) / len(source_points[cluster_index])

				f1_measure[cluster_index] = 2 * precisious[cluster_index] * float(recall[cluster_index]) / \
												(precisious[cluster_index] + recall[cluster_index])
				cluster_index += 1

		print("Precisious {}".format(precisious))
		print("Recall {}".format(recall))
		print("F1 measure {}".format(f1_measure))

		return [precisious, recall, f1_measure]

def main():
		# parametrs
		opt = parse_options()
		if opt is None:
				return
		# generate points
		print("Generating points..");
		source_points = []

		pg = PointGenerator()
		pg.enable_parabola(1, -5, 50)
		source_points.append(pg.generate_points(0, 4, 0, 1))

		pg.enable_parabola(1, -5, -30)
		source_points.append(pg.generate_points(0, 4, 0, 2))

		#pg.enable_line(1, 0)
		#source_points.append(pg.generate_points(6, 12, 1, 1))

		pg.enable_line(1, 5)
		source_points.append(pg.generate_points(4, 10, 0, 1))

		#pg.enable_sin(1, 1, 0)
		#source_points.append(pg.generate_points(5, 15, 2, 1))

#		pg.enable_sin(1, 1, 5)
#		source_points.append(pg.generate_points(5, 10, 0, 1))

		#source_points.append(pg.get_default_2D())
		all_points = []
		for p_list in source_points:
				for p in p_list:
						all_points.append(p)

		print("Generated {} points".format(len(all_points)))
		print("Dividing points to {} clusters..".format(opt['cluster_cnt']));
		classifier = Classificator(opt['type_dist'])
		classifier.hierarchy(all_points, int(opt['cluster_cnt']))

		result_p_clusters = []
		for c in classifier.clusters:
				result_p_clusters.append(c.points)

		print("Determine precision, recall, f1-measure..")
		count_measures(source_points, result_p_clusters)

		print("Showing clusters..")
		draw_cluster_points(result_p_clusters)

if __name__ == '__main__':
		sys.exit(main())
