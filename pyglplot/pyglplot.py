"""
Render using empty Vertexbuffer.
Renders 100 triangels emitted by a geometry shaders.
In addition we test if instancing is working passing gl_InstanceID from the vertex shader.
"""

# https://stackoverflow.com/questions/63086665/how-to-set-primitives-to-gl-lines-with-moderngl-in-python

from vispy import gloo, app
from vispy.gloo import Program
import numpy as np




class Line(gloo.VertexBuffer):
    """Line class
    """
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
        self._gScale = np.array([1.0, 0, 0, 1])
        self._gOffset = np.array([0.0, 0.0])

        self._program['pColor'] = self._color
        self._program['coordinates'] = self
        self._program['uOffset'] = self._offset
        self._program['uScale'] = self._scale

    def setColor(self, color: np.ndarray):
        self._color = color
        self._program['pColor'] = self._color

    def setScale(self, scaleX: float, scaleY: float):
        self._scale = np.array([scaleX, 0, 0, scaleY])
        self._program['uScale'] = self._scale * self._gScale

    def setOffset(self, offsetX: float, offsetY: float):
        self._offset = np.array([offsetX, offsetY])
        self._program['uOffset'] = self._offset + self._gOffset

    def setGlobalScale(self, scaleX: float, scaleY: float):
        self._gScale = np.array([scaleX, 0, 0, scaleY])
        self._program['uScale'] = self._scale * self._gScale

    def setGlobalOffset(self, offsetX: float, offsetY: float):
        self._gOffset = np.array([offsetX, offsetY])
        self._program['uOffset'] = self._offset + self._gOffset

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
    """Pyglplot class
    """
    def __init__(self):
        super().__init__(size=(512, 512), title='Rotating quad',
                         keys='interactive')
        # Build program & data
        self.lines = []
        if len(self.lines) == 0:
            self.lines.append(Line())

        self._gOffset = np.array([0.0, 0.0])
        self._gScale = np.array([1.0, 0, 0, 1])

        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_clear_color('black')

        self.timer = app.Timer('auto', self.on_timer)
        self.clock = 0
        self.timer.start()

        self.show()

    def setGlobalScale(self, scaleX: float, scaleY: float):
        for line in self.lines:
            line.setGlobalScale(scaleX, scaleY)

    def setGlobalOffset(self, offsetX: float, offsetY: float):
        for line in self.lines:
            line.setGlobalOffset(offsetX, offsetY)

    def on_draw(self, event):
        gloo.clear()
        for line in self.lines:
            line._program.draw(line._mode)

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)


    
    def eventLoop(self):
        pass

    def on_timer(self, event):
        self.eventLoop()
        self.update()
