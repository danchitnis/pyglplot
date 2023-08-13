import repackage
repackage.add_path('E:\\Code\\pyglplot\\')

from pyglplot import scatter
import numpy as np

import time

maxSquareNum = 100
squareSize = 0.02

plotScatter = scatter.Scatter(maxSquareNum, squareSize)




timeStamp = []


counter = 0

def update():
    timeStamp.append(time.perf_counter())

    global counter

    pos = np.array([np.random.rand(), np.random.rand()], dtype=np.float32)
    pos = pos * 2 - 1
    
    plotScatter.addPoint(pos)

    
    counter += 1

    

    if len(timeStamp) > 100:
        print(int(1/np.mean(np.diff(timeStamp))))
        timeStamp.clear()


plotScatter.run(update)
