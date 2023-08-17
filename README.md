[![PyPI version](https://badge.fury.io/py/pyglplot.svg)](https://badge.fury.io/py/pyglplot)

# pyglplot

A powerful Python plotting library that leverages OpenGL to provide exceptional performance and high-quality visualizations of 2D data. Based on the JavaScript library [webgl-plot](https://github.com/danchitnis/webgl-plot) this library is specifically designed for real-time plotting of line, scatter, and histogram plots. This library is cross-platform and works on Windows, Linux and Mac thanks to [GLFW](https://www.glfw.org/) windowing library. Furthermore, It is also compatible with Jupyter notebooks. This package is ideal for plotting realtime data from sensors and instruments, including streaming devices such as microphones and cameras, empowering users to analyze data as it is being generated.

## Installation

```bash
python -m pip install pyglplot
```

## Getting started

```python
import numpy as np
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

plot_line.run()
```

## Animating a plot

```python
import numpy as np
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

def update():
    y = 0.5*np.sin(np.pi*x) + np.random.rand(LINE_SIZE) * 0.1
    plot_line.update_line_y(0, y)

plot_line.run(update)
```

## License

MIT
