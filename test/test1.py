"""
Render using empty Vertexbuffer.
Renders 100 triangels emitted by a geometry shaders.
In addition we test if instancing is working passing gl_InstanceID from the vertex shader.
"""

# https://stackoverflow.com/questions/63086665/how-to-set-primitives-to-gl-lines-with-moderngl-in-python



import numpy as np

import repackage
repackage.up()

from pyglplot import pyglplot


#from ported._example import Example


class Example(pyglplot.Pyglplot):
    def setXY(self):
        self.x = np.linspace(-1, 1, 1000)
        self.y = np.sin(self.x * np.pi * 2) * 0.8 + \
            np.random.rand(len(self.x)) * 0.1


Example.run()
