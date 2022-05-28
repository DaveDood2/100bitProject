from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
import numpy as np
from matplotlib.ticker import LogFormatter
from math import ceil
from copy import copy





def animate(i, howFarBack):
    fig, ax = plt.subplots()
    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))
    line.set_ydata()
    return line,

def plotAnimatedLineGraph(data):
    ani = animation.FuncAnimation(
    fig, animate, interval=20, blit=True, save_count=50)
    plt.show()

def plotHeatMap(data, x_title='X Axis', y_title='Y Axis', title='', x_ticks=[], y_ticks=[]):
    plt.figure(figsize=(30,15))
    #xData, yData = zip(data)
    #print(xData, yData)
    positiveMin = data.min()
    tickMarks = []
    tickMarksString = []
    if (data.min() <= 0):
        positiveMin = 1
        tickMarks.append(positiveMin)
        tickMarksString.append(str(positiveMin))
    #Setting default (missing) color referenced from: https://matplotlib.org/2.0.2/examples/pylab_examples/image_masked.html
    palette = copy(plt.cm.viridis)
    palette.set_bad(palette.colors[0])
    plt.pcolor(data, cmap = palette, norm=colors.LogNorm(vmin=max(data.min(), 0.1), vmax=data.max()), snap=True)
    

    #plt.colorbar(ticks = np.arange(0, 19, step=2.5))
    #print("missing data is:", data[26][56])
    tickRange = 10
    tickPlacement = (data.max()-data.min()) / tickRange
    for i in range(0, tickRange):
        if (i > tickRange/2):
            if ((i % 2) == 1):
                continue
        tickMarks.append(ceil(tickPlacement*i+data.min()))
        tickMarksString.append(str(ceil(tickPlacement*i+data.min())))
    #Adding ticks to logarithmic colorbar referenced from: https://stackoverflow.com/questions/27345005/log-labels-on-colorbar-matplotlib
    #formatter = LogFormatter(10, labelOnlyBase=False) 
    #cbar = plt.colorbar(ticks = tickMarks, format = formatter)
    cbar = plt.colorbar(ticks = tickMarks)
    cbar.ax.set_yticklabels(tickMarksString)  # vertically oriented colorbar
    
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    plt.xlim(0, 256)
    plt.ylim(192, 0)
    plt.show()