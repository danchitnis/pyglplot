# pyglplot
 
A high-performance OpenGL plotting library for Python. Works in Jupiter notebooks and in standalone Python scripts. Based on the JavaScript library [webgl-plot]().

## Installation

```bash
pip install pyglplot
```

## Getting started

```python
import pyglplot as glp
import numpy as np

# Create a Line object
line = glp.Line()
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Add data to the line
line.setXY(x, y)

# Create pyglplot window
win = glp.Pyglplot()

# Add the line to the window
win.addLine(line)

# Show the window
win.show()
```
