from pyglplot import plot
import numpy as np

from vispy import gloo, app



line1 = plot.Line()
line2 = plot.Line()

win = plot.Canvas([line1, line2])


line1.setColor([1, 0, 0])
line2.setColor([0, 1, 0])

win.setGlobalOffset(0, 0.5)
win.setGlobalScale(1, 0.6)

x = np.linspace(-1, 1, 1000)

def loop():
    y1 = np.sin(x * np.pi * 2) * 0.8 + \
        np.random.rand(len(x)) * 0.1

    y2 = np.cos(x * np.pi * 2) * 0.8 + \
        np.random.rand(len(x)) * 0.1

    line1.setXY(x, y1)
    line2.setXY(x, y2)

win.setEventLoop(loop)
win.show()

app.run()