import os
from flask import Flask, make_response
from convex_hull import *


app = Flask(__name__)

@app.route("/")
def get_hull():
	import StringIO
	import random
	
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
    
    	# create hull
	n = 1000
	points = numpy.random.randn(n,2)
	
	(m,i) = minimum(points[:,1],compare)
	corner = points[i]
	vect = numpy.concatenate((points[:i],points[i+1:])) - corner
	angles = numpy.zeros(n-1)
	angles[:] = vect[:,0]/(vect[:,0]**2+vect[:,1]**2)**(0.5)
	(tt,angl_sort_ind) = sort_quick(1-angles, compare)
	vect = vect[angl_sort_ind]
	vect = numpy.concatenate((numpy.zeros((1,2)),vect))
	
	hull_ind = [0,1]
	l=len(vect)
	i=2
	while i<=l:
		a=vect[hull_ind[-1]]-vect[hull_ind[-2]]
		b = vect[i%l]-vect[hull_ind[-1]]
		if left(a,b)>-1:
			hull_ind.append(i)
			i=i+1
		else:
			hull_ind.pop()

	hull_ind.pop()
	convex_hull = vect[hull_ind] + corner

	convex_hull = numpy.concatenate((convex_hull,numpy.reshape(corner,(-1,2))))
	
	# create return object 
	fig=Figure()
	ax=fig.add_subplot(111)
	ax.scatter(points[:,0],points[:,1])
	ax.plot(convex_hull[:,0],convex_hull[:,1], linewidth=2.0)	
	
	canvas=FigureCanvas(fig)
	png_output = StringIO.StringIO()
	canvas.print_png(png_output)
	response=make_response(png_output.getvalue())
	response.headers['Content-Type'] = 'image/png'
	
	return response
	
if __name__ == "__main__":
	app.run()
