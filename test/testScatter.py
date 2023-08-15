#import repackage
#repackage.add_path('E:\\Code\\pyglplot\\')

from pyglplot import scatter
import numpy as np

import time

maxSquareNum = 1_000
squareSize = 0.01
newDataNum = 1

plotScatter = scatter.Scatter(maxSquareNum, squareSize)




timeStamp = []


counter = 0

def update():
    timeStamp.append(time.perf_counter())

    global counter

    rand = np.random.rand(1, newDataNum * 2)
    pos = np.array(rand, dtype=np.float32)
    pos[0::2] = (2*pos[0::2] - 1) * plotScatter.aspectRatio
    pos[1::2] = 2*pos[1::2] - 1
    
    plotScatter.addPoint(pos)

    
    counter += 1

    if counter*newDataNum > maxSquareNum:
        counter = 0
        plotScatter.resetPos()

    
    if len(timeStamp) > 100:
        print(int(1/np.mean(np.diff(timeStamp))))
        timeStamp.clear()


plotScatter.run(update)
