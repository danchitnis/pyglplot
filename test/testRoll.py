#import repackage
#repackage.add_path('/home/danial/code/pyglplot/')

from pyglplot import roll
import numpy as np

import time

numLines = 100

plotRoll = roll.Roll(1000, numLines=numLines)


for i in range(numLines):
    plotRoll.setLineColor([np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)], i)


y = np.zeros(numLines)

timeStamp = []

k = 0.5

counter = 0


def update():
    timeStamp.append(time.perf_counter())
    global counter

    
    
    for i in range(numLines):
        y[i] = np.sin(counter/(numLines*100)+ i*k)

    plotRoll.addPoint(y)

    
    counter += 1

    

    if len(timeStamp) > 100:
        print(int(1/np.mean(np.diff(timeStamp))))
        timeStamp.clear()


plotRoll.run(update)
