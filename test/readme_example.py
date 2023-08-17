import os
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



# Create a Line object
LINE_SIZE = 2000
LINE_NUMBER = 1

plot_line = line.Line(LINE_SIZE, LINE_NUMBER)
x = np.linspace(-1, 1, LINE_SIZE)
y = np.sin(np.pi*x)

# Add data to the line
plot_line.update_color(0, [255, 0, 255])
plot_line.update_line_xy(0, x, y)

#plot_line.run()

def update():
    y = 0.5*np.sin(np.pi*x) + np.random.rand(LINE_SIZE) * 0.1
    plot_line.update_line_y(0, y)

plot_line.run(update)