import os
import sys
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



LINE_SIZE = 1000

if len(sys.argv) < 2:
    CONTEXT_API = "auto"
else:
    CONTEXT_API = sys.argv[1]

plot_line = line.Line(LINE_SIZE, context_api=CONTEXT_API)

plot_line.update_color(0, 200, 200)

x = np.linspace(-1, 1, LINE_SIZE)
y = 0


def update():
    global y
    y = 0.5*np.sin(10*x) + np.random.rand(LINE_SIZE) * 0.1
    plot_line.update_line(x, y)


plot_line.run(update)
