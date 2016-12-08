from bokeh import mpl
from bokeh.plotting import output_file, show
from bokeh.embed import components

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

import sys,json

#Load the data that PHP sent us
try:
    file_name = sys.argv[1]
except:
    print "ERROR"
    sys.exit(1)

data_file = open(file_name, mode = 'r', buffering = 1024)
XData=[]
YData=[]
Height=[]
for line in data_file:
    if line[-1]=='\n':
        line=line[0:-1]
        line=line.split()
        XData.append(float(line[0]))
        YData.append(float(line[1]))
        Height.append(int(line[2]))

grid_x, grid_y = np.meshgrid(np.linspace(min(XData), max(XData), 100), np.linspace(min(YData), max(YData), 100))
grid_z = griddata((XData, YData), Height, (grid_x, grid_y), method = 'cubic')


plt.figure()
CS = plt.contour(grid_x, grid_y, grid_z)
plt.clabel(CS, inline=1, fontsize=10)
plt.title('Contour Map')

plot = mpl.to_bokeh()

#Get the components in the form of html codes
script, div = components(plot)

#When the double quotation marks exist in the PHP containing string, it will be converted to \", then they could not work in html, so here turn them as single quotation marks.
script_str = str(script).replace('"',"'")
div_str = str(div).replace('"',"'")

result = script_str + div_str

f = open('tt.txt', 'w')
f.write(result)

#Return the result to PHP
print json.dumps(result)

# show(mpl.to_bokeh())