import glfw
from OpenGL import GL as gl
import numpy as np

from . import common

class Roll():
    """Class to plot a rolling graph

    :param roll_buffer_size: number of points to plot
    :param num_lines: number of lines to plot
    :param width: window width
    :param height: window height
    :param title: window title
    :param context_api: OpenGL windowing method: "native", "egl", "osmesa", or "auto"

    """
    
    def __init__(self, roll_buffer_size = 100, num_lines = 1, width = 1280, height = 800, title = "pyglplot", context_api = "native"):

        self.roll_buffer_size = roll_buffer_size
        self.num_lines = num_lines

        vertex_shader_text = """
        # version 330
        layout(location = 1) in vec2 a_position;
        layout(location = 2) in vec3 a_color;

        uniform float uShift;

        out vec3 vColor;
            
        void main(void) {
            vec2 shiftedPosition = a_position - vec2(uShift, 0);
            gl_Position = vec4(shiftedPosition, 0, 1);

            vColor = a_color / vec3(255.0, 255.0, 255.0);

        }
        """

        fragment_shader_text = """
        # version 330
        precision mediump float;  
        in vec3 vColor;
        out vec4 outColor;
        
        void main()
        {
            gl_FragColor = vec4(vColor, 0.8);
        }
        """

        
        self.window = common.create_window(width, height, title, context_api)

        self.program = common.create_shaders(vertex_shader_text, fragment_shader_text)


        self.vertex_buffer = np.zeros( (self.roll_buffer_size + 2) * 2 * self.num_lines, dtype=np.uint32)
        self.color_buffer = np.ones( (self.roll_buffer_size + 2) * 3 * self.num_lines, dtype=np.uint8) * 255

        
        
        self.cbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.color_buffer.nbytes, self.color_buffer, gl.GL_STATIC_DRAW)

        self.colorLocation = gl.glGetAttribLocation(self.program, "a_color")
        gl.glVertexAttribPointer(self.colorLocation, 3, gl.GL_UNSIGNED_BYTE, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(self.colorLocation)



        self.vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertex_buffer.nbytes, self.vertex_buffer, gl.GL_DYNAMIC_DRAW)

        self.positionLocation = gl.glGetAttribLocation(self.program, "a_position")
        gl.glVertexAttribPointer(self.positionLocation, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(self.positionLocation)

        self.uShiftLocation = gl.glGetUniformLocation(self.program, "uShift")

        gl.glUseProgram(self.program)

        gl.glClearColor(0.1, 0.1, 0.1, 1.0)

        self.shift = 0
        self.data_x = 1
        self.data_index = 0

        self.last_data_X = np.zeros(num_lines)
        self.last_data_y = np.zeros(num_lines)

        glfw.set_window_size_callback(self.window, self.resize)

    
    def resize(self, window, width, height):
        gl.glViewport(0, 0, width, height)


    def add_point(self, y) -> None:
        """Add a point to the plot

        :param y: y value to plot

        """

        bf_size = self.roll_buffer_size + 2

        self.shift += 2 / self.roll_buffer_size
        self.data_x += 2 / self.roll_buffer_size

        gl.glUniform1f(self.uShiftLocation, self.shift)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        for i in range(self.num_lines):
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, (self.data_index + bf_size*i) *2 *4, np.array([self.data_x, y[i]], dtype=np.float32))

        if self.data_index == self.roll_buffer_size - 1:
            for i in range(self.num_lines):
                self.last_data_X[i] = self.data_x
                self.last_data_y[i] = y[i]

        if self.data_index == 0 and self.last_data_X[0] != 0:
            for i in range(self.num_lines):
                gl.glBufferSubData(gl.GL_ARRAY_BUFFER, (self.roll_buffer_size + bf_size*i) * 2 * 4, np.array([self.last_data_X[i], self.last_data_y[i], self.data_x, y[i]], dtype=np.float32))

        gl.glEnableVertexAttribArray(self.positionLocation)

        
        self.data_index = (self.data_index + 1) % self.roll_buffer_size

    def update_line_color(self, index_line, color: np.ndarray,) -> None:
        """Update the color of a line

        :param index_line: index of the line to update
        :param color: numpy array of 3 uint8 values (RGB) between 0 and 255 e.g.

        """

        gl.glUseProgram(self.program)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)

        for i in range(self.roll_buffer_size + 2):
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, (self.roll_buffer_size + 2)*index_line*3 + i*3, np.array(color, dtype=np.uint8))

        gl.glEnableVertexAttribArray(self.colorLocation)

    


    def run(self, update_function) -> None:
        """Run the plot

        :param update_function: function to call to update the plot

        """

        while not glfw.window_should_close(self.window):
            # Render here, e.g. using pyOpenGL
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            update_function()

            bfsize = self.roll_buffer_size + 2

            for i in range(self.num_lines):
                gl.glDrawArrays(gl.GL_LINE_STRIP, i*bfsize, self.data_index)
                gl.glDrawArrays(gl.GL_LINE_STRIP, i*bfsize + self.data_index, self.roll_buffer_size - self.data_index)
                gl.glDrawArrays(gl.GL_LINE_STRIP, i*bfsize + self.roll_buffer_size, 2)

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()
        print("Done!")

    