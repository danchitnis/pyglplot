"""
Render using empty Vertexbuffer.
Renders 100 triangels emitted by a geometry shaders.
In addition we test if instancing is working passing gl_InstanceID from the vertex shader.
"""

# https://stackoverflow.com/questions/63086665/how-to-set-primitives-to-gl-lines-with-moderngl-in-python

from vispy import gloo, app
from vispy.gloo import Program
import numpy as np

class Hello:
    def __init__(self):
        print("Hello")


class Pyglplot(app.Canvas):
    def __init__(self):
        super().__init__(size=(512, 512), title='Rotating quad',
                         keys='interactive')
        # Build program & data
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

        self._x = np.array([-1, 1])
        self._y = np.array([1, -1])
        self._rgb = np.array([1, 0.5, 0.5])

        self._program = Program(self._vertex, self._fragment)
        self._program['pColor'] = self._rgb
        self._program['coordinates'] = np.dstack([self._x,self._y]).astype('f4')
        self._program['uOffset'] = [0.0, 0.0]
        self._program['uScale'] = np.array([1.0, 0, 0, 1])

        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_clear_color('black')

        self.timer = app.Timer('auto', self.on_timer)
        self.clock = 0
        self.timer.start()

        self.show()

    def on_draw(self, event):
        gloo.clear()
        self._program.draw('line_strip')

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)

    
    def setXY(self, x: np.ndarray , y: np.ndarray):
        self._x = x
        self._y = y
        self._program['coordinates'] = np.dstack([self._x,self._y]).astype('f4')
    
    def eventLoop(self):
        pass

    def on_timer(self, event):
        self.eventLoop()
        self._program['pColor'] = self._rgb
        self.update()
