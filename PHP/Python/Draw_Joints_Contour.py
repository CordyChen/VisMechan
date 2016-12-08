from bokeh import mpl
from bokeh.embed import components
from bokeh.plotting import figure, show, output_file, hplot
from bokeh.models import Label

import matplotlib
import matplotlib.pyplot as plt 
import numpy as np
from scipy import interpolate

import sys,json


def Contour(filename):
    #readfile
    fileRead=open(filename,'r')
    Qx={}
    Qj={}
    Id=0
    for lineRead in fileRead:
        if lineRead[-1]=='\n':
            line=lineRead[0:-1]
            line=line.split()
            if line[0]!='#':
                Qx[Id]=float(line[1])*np.pi/180
                Qj[Id]=float(line[2])*np.pi/180
                Id=Id+1

    #point
    numberOfPoint=0
    xPoint={}
    yPoint={}
    while numberOfPoint < Id:
        xPoint[numberOfPoint]=np.sqrt(2.0)*np.sin(Qj[numberOfPoint]/2)*np.sin(Qx[numberOfPoint])
        yPoint[numberOfPoint]=np.sqrt(2.0)*np.sin(Qj[numberOfPoint]/2)*np.cos(Qx[numberOfPoint])
        numberOfPoint=numberOfPoint+1

    #build
    x=np.linspace(-1,1,21)
    y=np.linspace(-1,1,21)
    X,Y=np.meshgrid(x,y)
    Z=np.zeros(X.shape)

    #caculate
    for i in range(21):
        for j in range(21):
            xCaculate=i/10.0-1.1
            yCaculate=j/10.0-1.1
            z=0
            if xCaculate**2+yCaculate**2>1:
                Z[j,i]=0
            elif xCaculate**2+yCaculate**2<=0.81:
                nOfPoint=0
                for nOfPoint in range(Id):
                    if (xCaculate-xPoint[nOfPoint])**2+(yCaculate-yPoint[nOfPoint])**2<=0.01:
                        z=z+1
                Z[j,i]=z
            else:
                nOfPoint=0
                for nOfPoint in range(Id):
                    if (xCaculate-xPoint[nOfPoint])**2+(yCaculate-yPoint[nOfPoint])**2<=0.01:
                        z=z+1
                    radius=(xCaculate**2+yCaculate**2)**0.5
                    radiusNew=2-radius
                    xCaculate=-1*xCaculate*radiusNew/radius
                    yCaculate=-1*yCaculate*radiusNew/radius
                    if (xCaculate-xPoint[nOfPoint])**2+(yCaculate-yPoint[nOfPoint])**2<=0.01:
                       z=z+1
                Z[j,i]=z
    grid_x = np.linspace(-1, 1, 300)
    grid_y = np.linspace(-1, 1, 300)
    f = interpolate.interp2d(x, y, Z, kind='cubic')
    grid_z = f(grid_x, grid_y)
    plot = figure(width = 560, height = 560, x_range = (-1.2, 1.5), y_range = (-1.2, 1.5))
    
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


    # To plot the image
    plot.image(image = [grid_z], x = -1, y = -1, dw = 2, dh = 2, palette = 'Spectral10')


    # getwhite
    lowerband_x = np.cos(np.linspace(0,2*np.pi,360))
    lowerband_y = np.sin(np.linspace(0,2*np.pi,360))
    upperband_x = 1.5*np.cos(np.linspace(0,2*np.pi,360))
    upperband_y = 1.5*np.sin(np.linspace(0,2*np.pi,360))

    # Bollinger shading glyph:
    band_x = np.append(lowerband_x, upperband_x[::-1])
    band_y = np.append(lowerband_y, upperband_y[::-1])

    # Plot the shading
    plot.patch(band_x, band_y, color='white', fill_alpha=1)

    # To draw the colorbar
    bar_x = [1.1, 1.2]
    bar_y = np.linspace(0.3, 1.2, 10)
    bar_xx, bar_yy = np.meshgrid(bar_x, bar_y)
    bar_z = bar_yy
    plot.image(image = [bar_z], x = 1.15, y = 0.3, dw = 0.1, dh = 1, palette = 'Spectral10')
    labels_bar = {}
    i = 0
    while i < 10:
        bar_text = str(int(np.min(Z) + ((np.max(Z) - np.min(Z))*i)/9))
        bar_loc_y = 0.25 + i/10.0
        labels_bar[i] = Label(x = 1.25, y = bar_loc_y, text = bar_text, render_mode = 'canvas')
        plot.add_layout(labels_bar[i])
        i += 1

    #Plot the circle axes
    i = 0
    cir_x = []
    cir_y = []
    while i < 2.005*np.pi:
        cir_x += [np.cos(i)]
        cir_y += [np.sin(i)]
        i += np.pi/120
    plot.line(x = cir_x, y = cir_y, color="black", line_width = 3)

    # To draw the minor tick label
    i = 0
    j = 0
    distance_x = 0
    distance_y = 0
    labels_axes = {}
    while i < 2*np.pi:
        plot.line(x = [np.cos(i), 1.05*np.cos(i)], y = [np.sin(i), 1.05*np.sin(i)], color="black", line_width = 3)
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

    # To draw the main tick label
    labels1 = Label(x = 1.11, y = -0.04, text = 'E', render_mode = 'canvas')
    labels2 = Label(x = -1.18, y = -0.04, text = 'W', render_mode = 'canvas')
    labels3 = Label(x = -0.02, y = 1.1, text = 'N', render_mode = 'canvas')
    labels4 = Label(x = -0.02, y = -1.18, text = 'S', render_mode = 'canvas')
    plot.add_layout(labels1)
    plot.add_layout(labels2)
    plot.add_layout(labels3)
    plot.add_layout(labels4)

    return(plot)


# Load the data that PHP sent us
try:
    file_name = sys.argv[1]
except:
    print "ERROR"
    sys.exit(1)

# file_name = "upload_temp/20160820095259Joints.txt"
p0 = Contour(file_name)

# plot = mpl.to_bokeh()

#Get the components in the form of html codes
script, div = components(p0)

# #When the double quotation marks exist in the PHP containing string, it will be converted to \", then they could not work in html, so here turn them as single quotation marks.
script_str = str(script).replace('"',"'")
div_str = str(div).replace('"',"'")

result = script_str + div_str

f = open('tt.txt', 'w')
f.write(result)

#Return the result to PHP
print json.dumps(result)

# show(mpl.to_bokeh())