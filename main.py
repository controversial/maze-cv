from CV import *
from pathfinding import *
reload(perspective)
import photos

p = photos.pick_image().resize((800,600))
corners = redFinder.cornerCoords(p)
print corners
p2=perspective.transform(corners,perspective.squarecorners(p),p).crop((0,0,600,600))
print 'transformed'
p2.show()
