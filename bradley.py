from PIL import Image
import copy
import time

def bradley_threshold(image, threshold=75, windowsize=5):
	ws = windowsize
	image2 = copy.copy(image).convert('L')
	w, h = image.size
	l = image.convert('L').load()
	l2 = image2.load()
	threshold /= 100.0
	for y in xrange(h):
		for x in xrange(w):
			#find neighboring pixels
			neighbors =[(x+x2,y+y2) for x2 in xrange(-ws,ws) for y2 in xrange(-ws, ws) if x+x2>0 and x+x2<w and y+y2>0 and y+y2<h]
			#mean of all neighboring pixels
			mean = sum((l[a,b] for a,b in neighbors))/sum(1 for _ in neighbors)
			if l[x, y] < threshold*mean:
				l2[x,y] = 0
			else:
				l2[x,y] = 255
	return image2
	
if __name__ == '__main__':
	p = Image.open('Test Images/test.jpg')
	p.show()
	a=time.time()
	bradley_threshold(p, 75, 5).show()
	print time.time()-a
	
	a=time.time()
	bradley_threshold(p, 75, 10).show()
	print time.time()-a

	a=time.time()

	bradley_threshold(p, 75, 15).show()
	print time.time()-a
	
	a=time.time()
	bradley_threshold(p, 75, 20).show()
	print time.time()-a
