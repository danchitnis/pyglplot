#import repackage
#repackage.add_path('E:\\Code\\pyglplot\\')

from pyglplot import roll
import numpy as np

import time

numLines = 3

plotRoll = roll.Roll(2000, numLines=numLines)


for i in range(numLines):
    plotRoll.setLineColor([np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)], i)


y = np.zeros(numLines)

timeStamp = []

k = 1

counter = 0

def update():
    timeStamp.append(time.perf_counter())

    global counter
    
    for i in range(numLines):
        a = y[i] + 0.01 * (i+1) / numLines
        y[i] = a - np.round(a)

    plotRoll.addPoint(y)

    
    counter += 1

    

    if len(timeStamp) > 100:
        print(int(1/np.mean(np.diff(timeStamp))))
        timeStamp.clear()


plotRoll.run(update)
