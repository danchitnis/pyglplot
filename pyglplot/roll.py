import glfw
from OpenGL import GL as gl
import numpy as np

class Roll():
    
    def __init__(self, rollBufferSize = 100, numLines = 1):

        self.rollBufferSize = rollBufferSize
        self.numLines = numLines

        vertex_shader_text = """
        # version 330
        layout(location = 1) in vec2 a_position;
        uniform float uShift;
        uniform vec4 uColor;


            
        void main(void) {
            vec2 shiftedPosition = a_position - vec2(uShift, 0);
            gl_Position = vec4(shiftedPosition, 0, 1);

        }
        """

        fragment_shader_text = """
        # version 330
        precision mediump float;  
        void main()
        {
            gl_FragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """


        self.vertex_buffer = np.zeros( (self.rollBufferSize + 2) * 2 * self.numLines, dtype=np.uint32)

        if not glfw.init():
            exit()
        # Create a windowed mode window and its OpenGL context
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 1)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)

        #glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.EGL_CONTEXT_API)
        #glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.OSMESA_CONTEXT_API)


        self.window = glfw.create_window(1280, 800, "pyglplot", None, None)
        if not self.window:
            glfw.terminate()
            exit()
        # Make the window's context current
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        print(glfw.get_version_string())
        print(gl.glGetString(gl.GL_VERSION))

        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex_shader, vertex_shader_text)
        gl.glCompileShader(vertex_shader)

        success = gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS)
        if not success:
            print("Shader compilation failed")
            print(gl.glGetShaderInfoLog(vertex_shader))
        
        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragment_shader, fragment_shader_text)
        gl.glCompileShader(fragment_shader)

        success = gl.glGetShaderiv(fragment_shader, gl.GL_COMPILE_STATUS)
        if not success:
            print("Shader compilation failed")
            print(gl.glGetShaderInfoLog(fragment_shader))
        
        self.program = gl.glCreateProgram()
        gl.glAttachShader(self.program, vertex_shader)
        gl.glAttachShader(self.program, fragment_shader)
        gl.glLinkProgram(self.program)

        self.vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertex_buffer.nbytes, self.vertex_buffer, gl.GL_STATIC_DRAW)

        self.positionLocation = gl.glGetAttribLocation(self.program, "a_position")
        gl.glVertexAttribPointer(self.positionLocation, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(self.positionLocation)

        self.uShiftLocation = gl.glGetUniformLocation(self.program, "uShift")

        gl.glUseProgram(self.program)

        gl.glClearColor(0.1, 0.1, 0.1, 1.0)

        self.shift = 0
        self.dataX = 1
        self.dataIndex = 0

        self.lastDataX = np.zeros(numLines)
        self.lastDataY = np.zeros(numLines)



    def addPoint(self, y):
        bfSize = self.rollBufferSize + 2

        self.shift += 2 / self.rollBufferSize
        self.dataX += 2 / self.rollBufferSize

        gl.glUniform1f(self.uShiftLocation, self.shift)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        for i in range(self.numLines):
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, (self.dataIndex + bfSize*i) *2 *4, np.array([self.dataX, y[i]], dtype=np.float32))

        if self.dataIndex == self.rollBufferSize - 1:
            for i in range(self.numLines):
                self.lastDataX[i] = self.dataX
                self.lastDataY[i] = y[i]

        if self.dataIndex == 0 and self.lastDataX[0] != 0:
            for i in range(self.numLines):
                gl.glBufferSubData(gl.GL_ARRAY_BUFFER, (self.rollBufferSize + bfSize*i) * 2 * 4, np.array([self.lastDataX[i], self.lastDataY[i], self.dataX, y[i]], dtype=np.float32))

        gl.glEnableVertexAttribArray(self.positionLocation)

        
        self.dataIndex = (self.dataIndex + 1) % self.rollBufferSize
    


    def run(self, updateFunc):
        while not glfw.window_should_close(self.window):
            # Render here, e.g. using pyOpenGL
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            updateFunc()

            bfsize = self.rollBufferSize + 2

            for i in range(self.numLines):
                gl.glDrawArrays(gl.GL_LINE_STRIP, i*bfsize, self.dataIndex)
                gl.glDrawArrays(gl.GL_LINE_STRIP, i*bfsize + self.dataIndex, self.rollBufferSize - self.dataIndex)
                gl.glDrawArrays(gl.GL_LINE_STRIP, i*bfsize + self.rollBufferSize, 2)

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()
        print("Done!")

    