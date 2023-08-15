import glfw
from OpenGL import GL as gl
import numpy as np

class Scatter():
    
    def __init__(self, maxSqaureNum= 100, squareSize = 0.1):

        self.maxSqaureNum = maxSqaureNum
        self.squareSize = squareSize

        vertex_shader_text = """
        #version 330
        layout (location = 1) in vec2 aPos;
        layout (location = 2) in vec3 aColor;

        uniform float uSize;
        uniform vec2 uOffset;
        uniform mat2 uScale;

        out vec3 vColor;
        
        void main()
        {
            vec2 squareVertices[4] = vec2[4](vec2(-1.0, 1.0), vec2(1.0, 1.0), vec2(-1.0, -1.0), vec2(1.0, -1.0));
            vec2 pos = uSize * squareVertices[gl_VertexID] + aPos;
            gl_Position = vec4((uScale * pos) + uOffset, 0.0, 1.0);

            vColor = aColor;
            vColor = aColor/ vec3(255.0, 255.0, 255.0);
        }
        """

        fragment_shader_text = """
        #version 330
        in vec3 vColor;
        out vec4 FragColor;
        void main()
        {
            FragColor = vec4(vColor, 0.7);
        }
        """


        self.squarePositions = np.zeros((self.maxSqaureNum * 2), dtype=np.float32)
        self.colors = np.ones( (self.maxSqaureNum * 3), dtype=np.uint8) * np.uint8(255)

        if not glfw.init():
            exit()
        # Create a windowed mode window and its OpenGL context
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 1)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)

        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
        #glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.EGL_CONTEXT_API)
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

        


        self.squareIndices = np.array([0, 1, 2, 2, 1, 3], dtype=np.uint8)

        self.ebo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.squareIndices.nbytes, self.squareIndices, gl.GL_STATIC_DRAW)


        self.vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.squarePositions.nbytes, self.squarePositions, gl.GL_DYNAMIC_DRAW)

        self.positionLocation = gl.glGetAttribLocation(self.program, "aPos")
        gl.glVertexAttribPointer(self.positionLocation, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glVertexAttribDivisor(self.positionLocation, 1)
        gl.glEnableVertexAttribArray(self.positionLocation)

        self.initColor()

        self.cbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.colors.nbytes, self.colors, gl.GL_DYNAMIC_DRAW)

        self.colorLocation = gl.glGetAttribLocation(self.program, "aColor")
        gl.glVertexAttribPointer(self.colorLocation, 3, gl.GL_UNSIGNED_BYTE, gl.GL_FALSE, 0, None)
        gl.glVertexAttribDivisor(self.colorLocation, 1)
        gl.glEnableVertexAttribArray(self.colorLocation)


        


        self.uSize = gl.glGetUniformLocation(self.program, "uSize")
        self.uOffset = gl.glGetUniformLocation(self.program, "uOffset")
        self.uScale = gl.glGetUniformLocation(self.program, "uScale")

        gl.glUseProgram(self.program)

        self.windowSize = glfw.get_window_size(self.window)
        print(self.windowSize)
        self.aspectRatio = self.windowSize[0] / self.windowSize[1]

        gl.glUniform1f(self.uSize, np.float32(squareSize))
        gl.glUniform2f(self.uOffset, 0.0, 0.0)
        gl.glUniformMatrix2fv(self.uScale, 1, gl.GL_FALSE, np.array([[float(1/self.aspectRatio), 0.0], [0.0, 1.0]], dtype=np.float32))


        gl.glClearColor(0.1, 0.1, 0.1, 1.0)

        



        glfw.set_window_size_callback(self.window, self.resize)

        self.headIndex = 0

    
    def resize(self, window, width, height):
        gl.glViewport(0, 0, width, height)
        self.aspectRatio = width / height
        self.windowSize = (width, height)
        gl.glUniformMatrix2fv(self.uScale, 1, gl.GL_FALSE, np.array([[float(1/self.aspectRatio), 0.0], [0.0, 1.0]], dtype=np.float32))

    def initColor(self):
        self.colors = np.random.randint(0, 255, (self.maxSqaureNum * 3), dtype=np.uint8)


    def addPoint(self, pos:np.ndarray):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, self.headIndex * 2 * 4, pos.nbytes, pos)
        gl.glEnableVertexAttribArray(self.positionLocation)

        self.headIndex = (self.headIndex + int(pos.size / 2)) % self.maxSqaureNum

    def addPosAndColor(self, pos:np.ndarray, color:np.ndarray):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, self.headIndex * 2 * 4, pos.nbytes, pos)
        gl.glEnableVertexAttribArray(self.positionLocation)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, self.headIndex * 3, color.nbytes, color)
        gl.glEnableVertexAttribArray(self.colorLocation)

        self.headIndex = (self.headIndex + int(pos.size / 2)) % self.maxSqaureNum

    def resetPos(self):
        self.headIndex = 0
        self.squarePositions = self.squarePositions * 0.0

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.squarePositions.nbytes, self.squarePositions)
        gl.glEnableVertexAttribArray(self.positionLocation)

    def resetColor(self):
        self.colors = self.colors * np.uint8(255)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.colors.nbytes, self.colors)
        gl.glEnableVertexAttribArray(self.colorLocation)


    def updateEmpty():
        pass
        


    def run(self, updateFunc = updateEmpty):
        while not glfw.window_should_close(self.window):
            # Render here, e.g. using pyOpenGL
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            updateFunc()

            gl.glDrawElementsInstanced(gl.GL_TRIANGLES, self.squareIndices.size, gl.GL_UNSIGNED_BYTE, None, self.maxSqaureNum)

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()
        print("Done!")

    