"""
Render using empty Vertexbuffer.
Renders 100 triangels emitted by a geometry shaders.
In addition we test if instancing is working passing gl_InstanceID from the vertex shader.
"""

# https://stackoverflow.com/questions/63086665/how-to-set-primitives-to-gl-lines-with-moderngl-in-python

from vispy import gloo, app
from vispy.gloo import Program
import numpy as np


class LineStrip(gloo.VertexBuffer):
    def __init__(self):
        self._vertex = """
            #version 330
            attribute vec2 coordinates;
                        
            uniform mat2 uScale;
            uniform vec2 uOffset;
                        
            void main(void) {
                vec2 line = uScale * coordinates + uOffset;
                gl_Position = vec4(line, 0.0, 1.0);
            }
            """

        self._fragment = """
            #version 330
            uniform vec3 pColor;
            void main(void) {
                gl_FragColor =  vec4(pColor, 1);
            }
            """
        super().__init__()
        self._mode = 'line_strip'
        self._x = np.array([-1, 1])
        self._y = np.array([1, -1])
        self._data = np.dstack([self._x, self._y]).astype('f4')
        self._color = np.array([1, 1, 1])
        self._program = Program(self._vertex, self._fragment)
        self._scale = np.array([1.0, 0, 0, 1])
        self._offset = np.array([0.0, 0.0])
        self._program['pColor'] = self._color
        self._program['coordinates'] = self
        self._program['uOffset'] = self._offset
        self._program['uScale'] = self._scale

    def setColor(self, color: np.ndarray):
        self._color = color

    def setX(self, x: np.ndarray):
        self._x = x
        self._update()

    def setY(self, y: np.ndarray):
        self._y = y
        self._update()

    def setXY(self, x: np.ndarray, y: np.ndarray):
        self._x = x
        self._y = y
        self._update()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value
        self._update()

    def _update(self):
        self._data = np.dstack([self._x, self._y]).astype('f4')
        #self._data = self._data.reshape(-1, 2)
        #self._data = np.dstack([self._data[:, 0], self._data[:, 1]]).astype('f4')
        #self._data = self._data.reshape(-1, 2)
        #self._data = self._data.astype('f4')
        self.set_data(self._data)

    def append(self, value):
        self._data = np.append(self._data, value)
        self._update()

    def extend(self, value):
        self._data = np.append(self._data, value)
        self._update()

    def insert(self, index, value):
        self._data = np.insert(self._data, index, value)
        self._update()

    def pop(self, index):
        self._data = np.delete(self._data, index)
        self._update()

    def remove(self, value):
        self._data = np.delete(self._data, np.where(self._data == value))
        self._update()

    def __delitem__(self, key):
        self._data = np.delete(self._data, key)
        self._update()

    def __iadd__(self, other):
        self._data = np.append(self._data, other)
        self._update()
        return self

    def __imul__(self, other):
        self._data = np.repeat(self._data, other)
        self._update()
        return self

    def __add__(self, other):
        self._data = np.append(self._data, other)
        self._update()
        return self

    def __mul__(self, other):
        self._data = np.repeat(self._data, other)
        self._update()
        return self

    def __repr__(self):
        return self._data.__repr__()

    def __str__(self):
        return

class Pyglplot(app.Canvas):
    def __init__(self):
        super().__init__(size=(512, 512), title='Rotating quad',
                         keys='interactive')
        # Build program & data
        

        self._x = np.array([-1, 1])
        self._y = np.array([1, -1])
        self._rgb = np.array([1, 0.5, 0.5])

        self.line1 = LineStrip()
        self.line1.setXY(self._x, self._y)

        self.line2 = LineStrip()
        self.line2.setXY(self._x, self._y)
        #self.line._program = Program(self._vertex, self._fragment)

        #self._program = Program(self._vertex, self._fragment)
        #self.line._program['pColor'] = self._rgb
        #self.line._program['coordinates'] = self.line
        #self.line._program['uOffset'] = [0.0, 0.0]
        #self.line._program['uScale'] = np.array([1.0, 0, 0, 1])

        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_clear_color('black')

        self.timer = app.Timer('auto', self.on_timer)
        self.clock = 0
        self.timer.start()

        self.show()

    def on_draw(self, event):
        gloo.clear()
        self.line1._program.draw('line_strip')
        self.line2._program.draw('line_strip')

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)


    
    def eventLoop(self):
        pass

    def on_timer(self, event):
        self.eventLoop()
        self.update()
