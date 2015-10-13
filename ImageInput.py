# coding: utf-8
from PIL import Image
from Dijkstra import *

def find(color, im):
	'''Find all instances of a certain color in an image'''
	load = im.load()
	locations = []
	for y in range(im.size[1]):
		for x in range(im.size[0]):
			if load[x, y] == color:
				locations.append( (x, y) )
	return locations

def markPath(path, image):
	'''Draw in blue the provided path onto the provided image'''
	import copy
	i = copy.deepcopy(image)
	l = i.load()
	path.pop(0)# Remove the start square
	path.pop(-1) # Remove the finish square
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
	#Add connections by finding all neighboring pixels and checking if they exist in the image
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
        for name in ['maze1.png','maze2.png','maze3.png']:
                i = Image.open('Test Images/Mazes/'+name)
                i.resize((256,256)).show()
                graph, start, goal = GraphFromImage(i)
                path = [x.id for x in Dijkstra(graph, start, goal)]
                markPath(path, i).resize((256,256)).show()
