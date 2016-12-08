from random import random
import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, ColumnDataSource, Label
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

import sys,json

# Load the data that PHP sent us
try:
    filename = sys.argv[1]
except:
    print "ERROR"
    sys.exit(1)

# filename = "upload_temp/20160820095259Joints.txt"

# Get the data in the txt
fileRead=open(filename,'r')
Qx = {}
Qj = {}
Id = 0
for lineRead in fileRead:
    if lineRead[-1] == '\n':
        line = lineRead[0:-1]
        line = line.split()
        if line[0]!='#':
            Qx[Id] = float(line[1])*np.pi/180
            Qj[Id] = float(line[2])*np.pi/180
            Id = Id + 1

x = np.zeros(Id)
y = np.zeros(Id)
numberOfPoint = 0
while numberOfPoint < Id:
    x[numberOfPoint] = np.sqrt(2.0)*np.sin(Qj[numberOfPoint]/2)*np.sin(Qx[numberOfPoint])
    y[numberOfPoint] = np.sqrt(2.0)*np.sin(Qj[numberOfPoint]/2)*np.cos(Qx[numberOfPoint])
    numberOfPoint = numberOfPoint + 1

color = ["navy"] * len(x)
s1 = ColumnDataSource(data=dict(x = x, y = y, color = color))
p1 = figure(plot_width=480, plot_height=480, tools="lasso_select, reset, wheel_zoom", title="Scatter Map of Joints", x_axis_location=None, y_axis_location=None, x_range = (-1.2, 1.2), y_range = (-1.2, 1.2))

#Plot the circle axes
i = 0
cir_x = []
cir_y = []
while i < 2.005*np.pi:
    cir_x += [np.cos(i)]
    cir_y += [np.sin(i)]
    i += np.pi/120
p1.line(x = cir_x, y = cir_y, color="black", line_width = 3)

# To draw the minor tick label
i = 0
j = 0
distance_x = 0
distance_y = 0
labels_axes = {}
while i < 2*np.pi:
    p1.line(x = [np.cos(i), 1.05*np.cos(i)], y = [np.sin(i), 1.05*np.sin(i)], color="black", line_width = 3)
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
        p1.add_layout(labels_axes[j])
    i += np.pi/18
    j += 1

# To draw the main tick label
labels1 = Label(x = 1.11, y = -0.04, text = 'E', render_mode = 'canvas')
labels2 = Label(x = -1.18, y = -0.04, text = 'W', render_mode = 'canvas')
labels3 = Label(x = -0.02, y = 1.1, text = 'N', render_mode = 'canvas')
labels4 = Label(x = -0.02, y = -1.18, text = 'S', render_mode = 'canvas')
p1.add_layout(labels1)
p1.add_layout(labels2)
p1.add_layout(labels3)
p1.add_layout(labels4)

#To draw the scatter glyph
p1.circle('x', 'y', color = 'color', source=s1, alpha=0.4)

#To draw the histogram table
s2 = ColumnDataSource(data=dict(x = [], y = []))
p2 = figure(plot_width=480, plot_height=480,
            tools="pan, wheel_zoom", title="Histogram")
p2.quad(bottom = 'x', top = 'y', left = np.linspace(0, 355, 72), right = np.linspace(5, 360, 72), source=s2, alpha=0.3)

s1.callback = CustomJS(args=dict(s2=s2), code='''
        var inds = cb_obj.get('selected')['1d'].indices;
        var d1 = cb_obj.get('data');
        var d2 = s2.get('data');

        var Qx_1 = %s;

        d2['x'] = [];
        d2['y'] = [];
        var count = [];
        for (i = 0; i < d1['color'].length; i++) {
            d1['color'][i] = 'navy';
        }
        for (i = 0; i < 72; i ++)
            count[i] = 0;
        for (i = 0; i < inds.length; i++) {
            for (j = 0; j < 72; j++) {
                if ((Qx_1[inds[i]]*180/Math.PI) < (5*j + 5) && (Qx_1[inds[i]]*180/Math.PI) >= 5*j) {
                    count[j] += 1;
                    break;
                }
            }
            d1['color'][inds[i]] = 'firebrick';
        }
        for(j = 0; j < 72; j++) {
            d2['y'].push(count[j]);
            d2['x'].push(0);
        }
        s2.trigger('change');
    '''%Qx )

layout = row(p1, p2)

# show(layout)
#Get the components in the form of html codes
script, div = components(layout)

# print script
# print div

#When the double quotation marks exist in the PHP containing string, it will be converted to \", then they could not work in html, so here turn them as single quotation marks.
# script_str = str(script).replace('"',"'")
# div_str = str(div).replace('"',"'")

result = str(script) + str(div)

#Return the result to PHP
print json.dumps(result)