from bokeh import mpl
from bokeh.embed import components
from bokeh.plotting import figure, show, output_file
from bokeh.models import Label

import numpy as np

import sys,json

def Rose(filename):

    #To read the data file
    fileRead = open(filename,'r')
    Qx = {}
    Id = 0
    for lineRead in fileRead:
        if lineRead[-1] == '\n':
            line = lineRead[0:-1]
            line = line.split()
            if line[0] != '#':
                Qx[Id] = float(line[1])%180.0
                Id = Id + 1

    #To draw the grid circles
    plot = figure(width = 600, height = 400, x_range = (-1.3, 1.4), y_range = (-0.3, 1.5))
    R = np.linspace(0,1,6)
    for r in R:
        sigma = np.linspace(0,np.pi,360)
        xarr = []
        yarr = []
        for i in sigma:
            x1 = r*np.cos(i)
            y1 = r*np.sin(i)
            xarr.append(x1)
            yarr.append(y1)
        plot.line(x = xarr, y = yarr, color='black', line_width=1)

    # To draw the main tick label
    labels1 = Label(x = 1.03, y = -0.04, text = 'E', render_mode = 'canvas')
    labels2 = Label(x = -1.1, y = -0.04, text = 'W', render_mode = 'canvas')
    labels3 = Label(x = -0.02, y = 1.02, text = 'N', render_mode = 'canvas')
    labels4 = Label(x = 0.15, y = -0.1, text = '30', render_mode = 'canvas')
    labels5 = Label(x = 0.35, y = -0.1, text = '60', render_mode = 'canvas')
    labels6 = Label(x = 0.55, y = -0.1, text = '90', render_mode = 'canvas')
    labels7 = Label(x = 0.73, y = -0.1, text = '120', render_mode = 'canvas')
    labels8 = Label(x = 0.93, y = -0.1, text = '150', render_mode = 'canvas')
    plot.add_layout(labels1)
    plot.add_layout(labels2)
    plot.add_layout(labels3)
    plot.add_layout(labels4)
    plot.add_layout(labels5)
    plot.add_layout(labels6)
    plot.add_layout(labels7)
    plot.add_layout(labels8)

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

    #line
    alpha=np.linspace(0,np.pi,19)
    r1=np.linspace(0,1,2)
    for a in alpha:
        x2=r1*np.cos(a)
        y2=r1*np.sin(a)
        plot.line(x = x2, y = y2, color='black', line_width=1)

    #rose
    number=[0]*18
    for j in range(18): 
        for i in range(Id):
            if Qx[i]>=10*j and Qx[i]<10*(j+1):
                number[j]+=1        
        number[j]=float(number[j])/150.0

    x3=[None]*18
    y3=[None]*18
    for i in range(18):
        x3[i]=number[i]*np.cos((1-(5+10*i)/180.0)*np.pi)
        y3[i]=number[i]*np.sin((1-(5+10*i)/180.0)*np.pi)
    x3=[0]+x3
    y3=[0]+y3
    plot.patch(x3, y3, color='yellow', alpha = 0.5, line_width = 0)
    plot.line(x = x3+[0], y = y3+[0], color='black', line_width=2)

    return(plot)

# Load the data that PHP sent us
try:
    file_name = sys.argv[1]
except:
    print "ERROR"
    sys.exit(1)

# file_name = "upload_temp/20160820095259Joints.txt"
p0 = Rose(file_name)

# plot = mpl.to_bokeh()

#Get the components in the form of html codes
script, div = components(p0)

# #When the double quotation marks exist in the PHP containing string, it will be converted to \", then they could not work in html, so here turn them as single quotation marks.
script_str = str(script).replace('"',"'")
div_str = str(div).replace('"',"'")

result = script_str + div_str

#Return the result to PHP
print json.dumps(result)