import glfw
from OpenGL import GL as gl
import numpy as np

class Line():
    
    def __init__(self, lineSize = 100):

        self.lineSize = lineSize

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


        self.color_buffer = np.zeros( self.lineSize * 3, dtype=np.uint8)

        self.cbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.color_buffer.nbytes, self.color_buffer, gl.GL_STATIC_DRAW)

        self.colorLocation = gl.glGetAttribLocation(self.program, "a_color")
        gl.glVertexAttribPointer(self.colorLocation, 3, gl.GL_UNSIGNED_BYTE, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(self.colorLocation)

        
        self.vertex_buffer = np.zeros( self.lineSize * 2, dtype=np.uint32)


        self.vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertex_buffer.nbytes, self.vertex_buffer, gl.GL_DYNAMIC_DRAW)

        self.positionLocation = gl.glGetAttribLocation(self.program, "a_position")
        gl.glVertexAttribPointer(self.positionLocation, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(self.positionLocation)

        
        self.xy = np.zeros( self.lineSize * 2, dtype=np.float32)

        gl.glUseProgram(self.program)

        gl.glClearColor(0.1, 0.1, 0.1, 1.0)

        self.updateColor(255, 255, 0)

        glfw.set_window_size_callback(self.window, self.on_resize)

    
    def on_resize(self, window, width, height):
        gl.glViewport(0, 0, width, height)



    def updateColor(self, r, g, b):
        self.color_buffer[:] = r
        self.color_buffer[1::3] = g
        self.color_buffer[2::3] = b

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)

        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.color_buffer)

        gl.glEnableVertexAttribArray(self.colorLocation)



    def updateLine(self, x: np.ndarray, y: np.ndarray):
               
        self.xy[0::2] = x
        self.xy[1::2] = y
        
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.xy)

        gl.glEnableVertexAttribArray(self.positionLocation)

    
    def updateEmpty():
        pass

    def run(self, updateFunc = updateEmpty):
        while not glfw.window_should_close(self.window):
            # Render here, e.g. using pyOpenGL
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            updateFunc()

            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, self.lineSize)
        

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()
        print("Done!")

    