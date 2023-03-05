#import repackage
#repackage.add_path('/home/danial/code/pyglplot/')

from pyglplot import line
import numpy as np

lineSize = 1000

plotLine = line.Line(lineSize)

plotLine.updateColor(0,200,200)

x = np.linspace(-1, 1, lineSize)
y = 0

def update():
    global y
    y = 0.5*np.sin(10*x) + np.random.rand(lineSize) * 0.1
    plotLine.updateLine(x, y)

plotLine.run(update)