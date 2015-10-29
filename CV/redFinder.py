# One component at a time method

from PIL import Image, ImageFilter
from colorsys import rgb_to_hsv

def bfs(graph,start):
	# Breadth-first search to find pixels connected
	# graph is array with some pixels true and others false
	# start is x, y
	if not graph[start[0]][start[1]]:
		return
	visited = []
	w, h = len(graph)-1, len(graph[0])-1
	queue = [start]
	while queue:
		x, y = queue.pop(0)
		neighbors = []
		if x<w:
			neighbors.append((x+1,y))
		if x>0:
			neighbors.append((x-1,y))
		if y<h:
			neighbors.append((x,y+1))
		if y>0:
			neighbors.append((x,y-1))	
		for n in neighbors:
			if n not in visited and graph[n[0]][n[1]]:
				visited.append(n)
				queue.append(n)
	return visited
	
def rgb2hsv(*args):
	# RGB input out of (255,255,255)
	# HSV output out of (360,255,255)
	if len(args) == 1:
		r,g,b = [c/255.0 for c in args[0]]
	else:
		r,g,b = [c/255.0 for c in args]
	
	h,s,v = rgb_to_hsv(r,g,b)
	return h*360,s*255,v*255
	
def findRed(i):
	'''Return `clusters`, a list for each red object in `i` that
	contains all the pixel coordinates which make up that object'''
	i=i.convert('RGB')
	width,height=i.size
	#Apply gaussian blur
	blur = i.filter(ImageFilter.GaussianBlur(radius=max(i.size)/300))
	load = i.load()
	#Find red regions
	redMap = [[0 for _ in range(height)] for _ in range(width)]
	for y in range(height):
		for x in range(width):
			h,s,v=rgb2hsv(load[x,y])
			if (h < 20 or h > 330) and s > 100 and v > 100:
				redMap[x][y] = 1
	
	#Depth-first search on one pixel in each object to identify separate red objects		
	visited = []
	clusters = []
	for y in range(height):
		for x in range(width):
			if not (x, y) in visited:
				cluster = bfs(redMap, (x, y))
				if cluster is not None:
					clusters.append(cluster)
					visited += cluster
	#Exclude smaller clusters (accidental red pixels) so that clusters only include objects. 
	return [c for c in clusters if len(c)>10]

def resize(im, base=200):
	#Resize so the smaller image dimension is always 200
	if im.size[0] < im.size[1]:
		x = im.size[1]
		y = im.size[0]
		a = False
	else:
		x = im.size[0]
		y = im.size[1]
		a = True
	
	percent = (base/float(x))
	size = int((float(y)*float(percent)))
	if a:
		im = im.resize((base, int(size*0.5)), Image.ANTIALIAS)
	else:
		im = im.resize((size, int(base*0.5)), Image.ANTIALIAS)
	return im

def cornerCoords(image):
	'''Return inside corners of all red corners in image'''
	p = image.resize((100*image.size[0]/image.size[1], 100))
	#record scale of shrinkage	
	scale = [x/float(y) for x,y in zip(image.size, p.size)][0]
	
	#Find red objects
	clusters = findRed(p) 
	# only top 4 with aspect ratios closest to 1
	def aspect(cluster):
		x, y = zip(*cluster)
		w = max(x)-min(x)
		h = max(y)-min(y)
		return float(max(w,h))/float(min(w,h))
	squarest = sorted(clusters, key=aspect)[:4]
	XandYs = [zip(*c) for c in squarest]
	centers = [[int(sum(list(x))/len(list(x))) for x in c] for c in XandYs]
	
	topLeft,topRight=[squarest[centers.index(c)] for c in sorted(sorted(centers,key=lambda x:x[1])[:2],key=lambda x:x[0])]
	botLeft,botRight=[squarest[centers.index(c)] for c in sorted(sorted(centers,key=lambda x:x[1])[2:],key=lambda x:x[0])]
	
	def manhattan(xy,xy2):
		x,y=xy
		x2,y2=xy2
		return abs(x2-x)+abs(y2-y)
			
	tl = max(topLeft)
	bboxTR = min(zip(*topRight)[0]),max(zip(*topRight)[0])
	tr = min(topRight, key=lambda xy: manhattan(xy,bboxTR))
	bboxBL = max(zip(*botLeft)[0]),min(zip(*botLeft)[0])
	bl = min(botLeft, key=lambda xy: manhattan(xy,bboxBL))
	br = min(botRight)
	scaled= [tuple([int(c*scale) for c in point]) for point in [tl,tr,br,bl]]
	return scaled
	

if __name__ == '__main__':
	import photos, time
	inp = photos.pick_image()
	t = time.time()
	points = cornerCoords(inp)
	print time.time()-t
	out = inp.copy()
	
	import ImageDraw
	d = ImageDraw.Draw(out)
	d.line(points+[points[0]],fill=(255,255,0),width=10)
	
	out.show()
