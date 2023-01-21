# pyglplot
 
A high-performance OpenGL plotting library for Python. Works in Jupiter notebooks and standalone Python scripts. Based on the JavaScript library [webgl-plot](https://github.com/danchitnis/webgl-plot) and build upon [vispy](https://github.com/vispy/vispy) especially for plotting realtime line, scatter and histogram plots. Although other plotting libraries like [vispy](https://github.com/vispy/vispy) have plotting capabilities, pyglplot focuses on a simple and portable interface for plotting realtime data. The main uses are plotting realtime data from sensors and instruments, including streaming devices such as microphones and cameras.

## Installation

```bash
python -m pip install pyglplot
```

## Getting started (Jupyter notebook)

```python
import numpy as np
from pyglplot import plot

# Create a Line object
line = plot.Line()
x = np.linspace(-1, 1, 1000)
y = np.sin(x)

# Add data to the line
line.setXY(x, y)

# Create pyglplot window and add the line
win = plot.Canvas([line])

# Show the window
win
```

## Getting started (standalone Python script)

```python
import numpy as np
from pyglplot import plot
from vispy import app

# Create a Line object
line = plot.Line()
x = np.linspace(-1, 1, 1000)
y = np.sin(x)

# Add data to the line
line.setXY(x, y)

win = plot.Canvas([line])

app.run()
```

## Animating a plot

```python
line = plot.Line()

win = plot.Canvas([line])

line.setColor([1, 1, 0])

x = np.linspace(-1, 1, 1000)

# Define the event loop
def loop():
    y = np.sin(x * np.pi * 2) * 0.8 + \
        np.random.rand(len(x)) * 0.1
    line.setXY(x, y)

# Set the event loop to the window
win.setEventLoop(loop)

win
```

## Notice on Performance

The performance of pyglplot is dependent on various factors. Relative to its Javascript counterpart [webglplot](https://github.com/danchitnis/webgl-plot), it has faster computation since it is using [numpy](https://github.com/numpy/numpy), however, it has a more complex datapath compared to WebGL hence expected a slower performance. Additionally, the performance in Jupyter notebooks is slower than in standalone Python scripts. This slowdown is because there is no direct interface between the Javascript and Python kernel in Jupyter notebooks. Instead, the data is passed through the Jupyter kernel, a bottleneck. Here we use [jupyter_rfb](https://github.com/vispy/jupyter_rfb/), which creates an image interface to render OpenGL offscreen and transfer the image to the Jupyter notebook at high framerates. The performance in standalone Python scripts is much better since there is no such bottleneck.

If you are interested in a better user interface, such as buttons and controls in a more production-ready application, then use [webglplot](https://github.com/danchitnis/webgl-plot). If you focus on prototyping and interactive numerical computations, use [pyglplot](https://github.com/danchitnis/pyglplot).

## License

MIT
