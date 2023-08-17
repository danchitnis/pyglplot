import os
import sys
import time
import numpy as np

try:
    from pyglplot import line

except ImportError:
    print("ImportError: pyglplot not found")
    print("trying pyglplot from local folder")

    import repackage
    abs_path = os.getcwd()
    print("abs_path=", abs_path)
    repackage.add_path(abs_path)
    print("")

from pyglplot import line



LINE_SIZE = 2000
LINE_NUMBER = 3

if len(sys.argv) < 2:
    CONTEXT_API = "auto"
else:
    CONTEXT_API = sys.argv[1]

plot_line = line.Line(LINE_SIZE, LINE_NUMBER, context_api=CONTEXT_API)

for i in range(LINE_NUMBER):
    plot_line.update_color(i, [np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)])

x = np.linspace(-1, 1, LINE_SIZE)
for i in range(LINE_NUMBER):
    plot_line.update_line_x(i, x)

xlarge = np.array([x, x, x])
print("xlarge.shape=", xlarge.shape)
print(xlarge[0].shape)

timeStamp = []


def update():
    timeStamp.append(time.perf_counter())

    phase = 0.1* time.perf_counter() % 1
    
    for i in range(LINE_NUMBER):
        y = np.linspace(-1, 1/LINE_NUMBER, LINE_SIZE) + (2*i-np.floor(LINE_NUMBER/2))/LINE_NUMBER + 2* phase -1
        plot_line.update_line_y(i, y)

    if len(timeStamp) > 100:
        print(int(1/np.mean(np.diff(timeStamp))))
        timeStamp.clear()

plot_line.run(update)
