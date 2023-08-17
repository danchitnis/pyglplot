import glfw
from OpenGL import GL as gl
import numpy as np

from . import common

class Line():
    
    def __init__(self, line_size = 100, line_number = 1, width = 1280, height = 800, title = "pyglplot", context_api = "native"):

        self.line_size = line_size
        self.line_number = line_number

        vertex_shader_text = """
        # version 330
        layout(location = 1) in vec2 a_position;
        layout(location = 2) in vec3 a_color;

        out vec3 vColor;
            
        void main(void) {
            gl_Position = vec4(a_position, 0, 1);
            vColor = a_color/ vec3(255.0, 255.0, 255.0);
        }
        """

        fragment_shader_text = """
        # version 330
        precision mediump float;
        in vec3 vColor;
        out vec4 outColor;

        void main()
        {
            outColor = vec4(vColor,0.7);
        }
        """

        self.window = common.create_window(width, height, title, context_api)

        self.program = common.create_shaders(vertex_shader_text, fragment_shader_text)

        self.color_buffer = np.zeros( self.line_size * 3 * line_number, dtype=np.uint8)

        self.cbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.color_buffer.nbytes, self.color_buffer, gl.GL_STATIC_DRAW)

        self.color_location = gl.glGetAttribLocation(self.program, "a_color")
        gl.glVertexAttribPointer(self.color_location, 3, gl.GL_UNSIGNED_BYTE, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(self.color_location)

        
        self.vertex_buffer = np.zeros( self.line_size * 2 * self.line_number, dtype=np.float32)


        self.vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertex_buffer.nbytes, self.vertex_buffer, gl.GL_DYNAMIC_DRAW)

        self.position_location = gl.glGetAttribLocation(self.program, "a_position")
        gl.glVertexAttribPointer(self.position_location, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(self.position_location)

        

        gl.glUseProgram(self.program)

        gl.glClearColor(0.1, 0.1, 0.1, 1.0)

        self.buffer_single_line = np.zeros(self.line_size*2, dtype=np.float32)

        glfw.set_window_size_callback(self.window, self.on_resize)

    
    def on_resize(self, window, width, height):
        gl.glViewport(0, 0, width, height)



    def update_color(self, index_line: int, rgb: np.ndarray):

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)

        color = np.zeros(self.line_size*3, dtype=np.uint8)

        color[0::3] = rgb[0]
        color[1::3] = rgb[1]
        color[2::3] = rgb[2]

        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, index_line*self.line_size*3, color)
        
        gl.glEnableVertexAttribArray(self.color_location)



    def update_line_xy(self, index_line: int, x: np.ndarray, y: np.ndarray):

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        self.buffer_single_line[0::2] = x
        self.buffer_single_line[1::2] = y

        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, index_line*self.buffer_single_line.nbytes, self.buffer_single_line)

        gl.glEnableVertexAttribArray(self.position_location)

    
    def update_line_x(self, index_line: int, x: np.ndarray):

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        self.buffer_single_line[0::2] = x

        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, index_line*self.buffer_single_line.nbytes, self.buffer_single_line)

        gl.glEnableVertexAttribArray(self.position_location)

    
    def update_line_y(self, index_line: int, y: np.ndarray):

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        self.buffer_single_line[1::2] = y

        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, index_line*self.buffer_single_line.nbytes, self.buffer_single_line)

        gl.glEnableVertexAttribArray(self.position_location)

    
    def update_empty():
        pass

    def run(self, update_function = update_empty):
        while not glfw.window_should_close(self.window):
            # Render here, e.g. using pyOpenGL
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            update_function()

            for i in range(self.line_number):
                gl.glDrawArrays(gl.GL_LINE_STRIP, i*self.line_size, self.line_size)
        
            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()
        print("Done!")

    