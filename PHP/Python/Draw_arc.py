import numpy as np
from math import *

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Label
from bokeh.models import Arrow, VeeHead

import sys,json

#The function to draw the arc line of the joints
def arc(dip, dia, color, name):
    dip = dip*np.pi/180
    dia = dia*np.pi/180
    x_arc = np.tan(dia)*np.sin(dip)
    y_arc = np.tan(dia)*np.cos(dip)
    r_arc = 1/np.cos(dia)
    sigma = np.linspace(np.pi-dip+0.1,np.pi-dip+0.1+2*np.pi,360)
    xarr = []
    yarr = []
    for i in sigma:
        x1 = x_arc+r_arc*np.cos(i)
        y1 = y_arc+r_arc*np.sin(i)
        if x1**2+y1**2>=1:
            continue
        xarr += [x1]
        yarr += [y1]
    plot.line(x = [-np.cos(dip),xarr[0]], y =  [np.sin(dip),yarr[0]], color = color, line_width = 3)
    plot.line(x = [-np.cos(dip-np.pi),xarr[-1]], y =  [np.sin(dip-np.pi),yarr[-1]], color = color, line_width = 3)
    plot.line(x = xarr, y = yarr, color = color, line_width = 3)
    # plot.add_layout(Arrow(end = VeeHead(size = 8),line_width = 1.5, line_color = 'black', x_start = -(np.tan(np.pi/4-dia/2)*np.sin(dip)), y_start = (-np.tan(np.pi/4-dia/2)*np.cos(dip)), x_end = 0, y_end = 0))


# Load the data that PHP sent us
try:
    data = sys.argv[1]
except:
    print "ERROR"
    sys.exit(1)

#Get the list of the data
data_li = data.split(",")
# data_li = [23, 44, 156, 34, 277, 67]

#Plot the chart frame
plot = figure(width=600, height=600, x_range = (-1.2, 1.2), y_range = (-1.2, 1.2))
i = 0
cir_x = []
cir_y = []
while i < 2.005*np.pi:
	cir_x += [np.cos(i)]
	cir_y += [np.sin(i)]
	i += np.pi/120
plot.line(x = cir_x, y = cir_y, color="#7FC97F", line_width = 3)

i = 0
j = 0
distance_x = 0
distance_y = 0
labels_axes = {}
while i < 2*np.pi:
	plot.line(x = [np.cos(i), 1.05*np.cos(i)], y = [np.sin(i), 1.05*np.sin(i)], color="#7FC97F", line_width = 3)
        if j < 9:
            distance_x = 1.06*np.cos(i)
            distance_y = 1.06*np.sin(i)
        elif j > 27:
            distance_x = 1.06*np.cos(i) 
            distance_y = 1.06*np.sin(i) - 0.07
        elif j < 18:
            distance_x = 1.06*np.cos(i) - 0.09
            distance_y = 1.06*np.sin(i)
        else:
            distance_x = 1.06*np.cos(i) - 0.09
            distance_y = 1.06*np.sin(i) - 0.07
    	labels_axes[j] = Label(x = distance_x, y = distance_y, text = str(10*j), render_mode = 'canvas')
        if (j%9) != 0:
            plot.add_layout(labels_axes[j])
        i += np.pi/18
        j += 1

labels1 = Label(x = 1.11, y = -0.04, text = 'E', render_mode = 'canvas')
labels2 = Label(x = -1.18, y = -0.04, text = 'W', render_mode = 'canvas')
labels3 = Label(x = -0.02, y = 1.1, text = 'N', render_mode = 'canvas')
labels4 = Label(x = -0.02, y = -1.18, text = 'S', render_mode = 'canvas')
plot.add_layout(labels1)
plot.add_layout(labels2)
plot.add_layout(labels3)
plot.add_layout(labels4)

# To wipe off the axesof the figure
plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None
plot.xaxis.axis_label_text_color = None
plot.xaxis.axis_line_color = None
plot.xaxis.minor_tick_line_color = None
plot.xaxis.major_tick_line_color = None
plot.xaxis.major_label_text_color = None
plot.yaxis.axis_label_text_color = None
plot.yaxis.axis_line_color = None
plot.yaxis.minor_tick_line_color = None
plot.yaxis.major_tick_line_color = None
plot.yaxis.major_label_text_color = None


plot.circle(0, 0)
labels0 = Label(x = 0, y = 0, text = 'O', render_mode = 'canvas')
plot.add_layout(labels0)

#Draw the arc line from the data got from PHP
if (data_li[0] != '') and (data_li[1] != ''):
	arc(float(data_li[0]), float(data_li[1]), 'blue', 'Joints1')

if (data_li[2] != '') and (data_li[3] != ''):
	arc(float(data_li[2]), float(data_li[3]), 'blue', 'Joints2')

if (data_li[4] != '') and (data_li[5] != ''):
	arc(float(data_li[4]), float(data_li[5]), 'red', 'Slope')


#show(plot)

#Get the components in the form of html codes
script, div = components(plot)


#When the double quotation marks exist in the PHP containing string, it will be converted to \", then they could not work in html, so here turn them as single quotation marks.
script_str = str(script).replace('"',"'")
div_str = str(div).replace('"',"'")

result = script_str + div_str


#Return the result to PHP
print json.dumps(result)