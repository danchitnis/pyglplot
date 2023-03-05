#import repackage
#repackage.add_path('/home/danial/code/pyglplot/')

from pyglplot import roll
import numpy as np


plotRoll = roll.Roll(1000)

y = 0

def update():
    global y
    y += np.random.rand() * 0.1 - 0.05
    if y > 1:
        y = 1
    if y < -1:
        y = -1

    plotRoll.addPoint(y)


plotRoll.run(update)

