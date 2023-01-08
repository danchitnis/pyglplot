"""
Render using empty Vertexbuffer.
Renders 100 triangels emitted by a geometry shaders.
In addition we test if instancing is working passing gl_InstanceID from the vertex shader.
"""

# https://stackoverflow.com/questions/63086665/how-to-set-primitives-to-gl-lines-with-moderngl-in-python

import moderngl
import numpy as np
import moderngl_window as mglw


class Pyglplot(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "pyglplot"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True

    def __init__(self, **kwargs,):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 coordinates;
                void main(void) {
                    float x = coordinates.x;
                    float y = coordinates.y;
                    vec2 line = vec2(x, y);
                    gl_Position = vec4(line, 0.0, 1.0);
                }
            ''',

            fragment_shader='''
                #version 330
                precision mediump float;
                uniform highp vec4 uColor;
                void main(void) {
                    gl_FragColor =  vec4(1.0, 0.5, 0.5, 1.0);
                }
            ''',
        )
        self.x = np.array([0, 0])
        self.y = np.array([1, 1])

        self.doStuff()

        #self.vertices = np.array([[-1.0, -1.0, 0.6, 0.8]])

    def setXY(self):
        self.x = np.array([0, 0])
        self.y = np.array([1, 1])

    def doStuff(self):
        self.vertices = np.dstack([self.x, self.y])
        self.vbo = self.ctx.buffer(self.vertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(
            self.prog, self.vbo, 'coordinates')

        self.vertices2 = np.dstack([self.y, self.x])
        self.vbo2 = self.ctx.buffer(self.vertices2.astype('f4').tobytes())
        self.vao2 = self.ctx.simple_vertex_array(
            self.prog, self.vbo2, 'coordinates')

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)

        self.setXY()
        self.doStuff()

        self.vao.render(moderngl.LINE_STRIP)
        self.vao2.render(moderngl.LINE_STRIP)

    def resize(self, width: int, height: int):
        print("Window was resized. buffer size is {} x {}".format(width, height))
