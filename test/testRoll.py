import repackage
repackage.add_path('/home/danial/code/pyglplot/')

from pyglplot import roll
import numpy as np


plotRoll = roll.Roll(1000, 3)

plotRoll.setLineColor(np.array([255, 255, 0]), 0)
plotRoll.setLineColor(np.array([0, 255, 255]), 1)
plotRoll.setLineColor(np.array([255, 0, 255]), 2)

y = 0

def update():
    global y
    y += np.random.rand() * 0.1 - 0.05
    if y > 1:
        y = 1
    if y < -1:
        y = -1

    plotRoll.addPoint(np.array([y, y+0.1, y-0.1]))


plotRoll.run(update)

