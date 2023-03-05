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
lineSize = 1000
plotLine = line.Line(lineSize)
x = np.linspace(-1, 1, lineSize)
y = np.sin(x)

# Add data to the line
plotLine.updateLine(x, y)

plotLine.run()
```

## Animating a plot

```python
lineSize = 1000

plotLine = line.Line(lineSize)

x = np.linspace(-1, 1, lineSize)
y = 0

def update():
    global y
    y = 0.5*np.sin(10*x) + np.random.rand(lineSize) * 0.1
    plotLine.updateLine(x, y)

plotLine.run(update)
```

## License

MIT
