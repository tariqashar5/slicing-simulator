import math
import sys
from sklearn.neighbors import KDTree

def distance(a, b):
	p = (a.x, a.y)
	q = (b.x, b.y)
	return math.dist(p, q)

def kdtree(clients, basestations):
	client_coor = [(c.x, c.y) for c in clients]
	bs_coor = [(b.x, b.y) for b in basestations]

	tree = KDTree(bs_coor, leaf_size = 2)

	res = tree.query(client_coor)
	return res

def init_tree(basestations):
	bs_coor = [(b.x, b.y) for b in basestations]
	tree = KDTree(bs_coor, leaf_size = 2)
	return tree