# coding: utf-8
from PIL import Image
from Dijkstra import *

def find(color, im):
	load = im.load()
	locations = []
	for y in range(im.size[1]):
		for x in range(im.size[0]):
			if load[x, y] == color:
				locations.append( (x, y) )
	return locations
def markPath(path, image):
	import copy
	i = copy.deepcopy(image)
	l = i.load()
	for x, y in path:
		l[x, y] = (0,0,255)
	return i
def GraphFromImage(im):
	'''Create a graph from an image where black pixels are walls,
	white are paths, green is the start, and red is the end.'''
	start = find((0,255,0), im)[0]
	goal  = find((255,0,0), im)[0]
	path = find((255,255,255), im)
	path.append(start)
	path.append(goal)
	pathNodes = [Node(p) for p in path]
	graph = Graph(pathNodes)
	#construct graph
	for x, y in path:
		neighbors = [(x+1,y), (x-1, y), (x, y+1), (x, y-1)]
		node = pathNodes[path.index((x,y))]
		for n in neighbors:
			if n in path:
				node2 = pathNodes[path.index(n)]
				graph.add_connection(node, node2)
	startNode = pathNodes[path.index(start)]
	goalNode = pathNodes[path.index(goal)]
	return graph, startNode, goalNode

if __name__ == '__main__':
	i = Image.open('out.png')
	i.resize((256,256)).show()
	graph, start, goal = GraphFromImage(i)
	path = [x.id for x in Dijkstra(graph, start, goal)]
	markPath(path, i).resize((256,256)).show()