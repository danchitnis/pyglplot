import glfw
from OpenGL import GL as gl
import numpy as np

class Scatter():
    
    def __init__(self, max_square_num= 100, square_size = 0.1, width = 1280, height = 800, title = "pyglplot", context_api = "native"):

        self.max_square_num = max_square_num
        self.square_size = square_size

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


        self.square_positions = np.zeros((self.max_square_num * 2), dtype=np.float32)
        self.colors = np.ones( (self.max_square_num * 3), dtype=np.uint8) * np.uint8(255)

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

        


        self.square_indices = np.array([0, 1, 2, 2, 1, 3], dtype=np.uint8)

        self.ebo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.square_indices.nbytes, self.square_indices, gl.GL_STATIC_DRAW)


        self.vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.square_positions.nbytes, self.square_positions, gl.GL_DYNAMIC_DRAW)

        self.position_location = gl.glGetAttribLocation(self.program, "aPos")
        gl.glVertexAttribPointer(self.position_location, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glVertexAttribDivisor(self.position_location, 1)
        gl.glEnableVertexAttribArray(self.position_location)

        self.init_color()

        self.cbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.colors.nbytes, self.colors, gl.GL_DYNAMIC_DRAW)

        self.color_location = gl.glGetAttribLocation(self.program, "aColor")
        gl.glVertexAttribPointer(self.color_location, 3, gl.GL_UNSIGNED_BYTE, gl.GL_FALSE, 0, None)
        gl.glVertexAttribDivisor(self.color_location, 1)
        gl.glEnableVertexAttribArray(self.color_location)


        


        self.u_size = gl.glGetUniformLocation(self.program, "uSize")
        self.u_offset = gl.glGetUniformLocation(self.program, "uOffset")
        self.u_scale = gl.glGetUniformLocation(self.program, "uScale")

        gl.glUseProgram(self.program)

        self.window_size = glfw.get_window_size(self.window)
        print(self.window_size)
        self.aspect_ratio = self.window_size[0] / self.window_size[1]

        gl.glUniform1f(self.u_size, np.float32(square_size))
        gl.glUniform2f(self.u_offset, 0.0, 0.0)
        gl.glUniformMatrix2fv(self.u_scale, 1, gl.GL_FALSE, np.array([[float(1/self.aspect_ratio), 0.0], [0.0, 1.0]], dtype=np.float32))


        gl.glClearColor(0.1, 0.1, 0.1, 1.0)

        



        glfw.set_window_size_callback(self.window, self.resize)

        self.head_index = 0

    
    def resize(self, window, width, height):
        gl.glViewport(0, 0, width, height)
        self.aspect_ratio = width / height
        self.window_size = (width, height)
        gl.glUniformMatrix2fv(self.u_scale, 1, gl.GL_FALSE, np.array([[float(1/self.aspect_ratio), 0.0], [0.0, 1.0]], dtype=np.float32))

    def init_color(self):
        self.colors = np.random.randint(0, 255, (self.max_square_num * 3), dtype=np.uint8)


    def add_point(self, pos:np.ndarray):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, self.head_index * 2 * 4, pos.nbytes, pos)
        gl.glEnableVertexAttribArray(self.position_location)

        self.head_index = (self.head_index + int(pos.size / 2)) % self.max_square_num

    def add_pos_and_color(self, pos:np.ndarray, color:np.ndarray):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, self.head_index * 2 * 4, pos.nbytes, pos)
        gl.glEnableVertexAttribArray(self.position_location)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, self.head_index * 3, color.nbytes, color)
        gl.glEnableVertexAttribArray(self.color_location)

        self.head_index = (self.head_index + int(pos.size / 2)) % self.max_square_num

    def reset_pos(self):
        self.head_index = 0
        self.square_positions = self.square_positions * 0.0

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.square_positions.nbytes, self.square_positions)
        gl.glEnableVertexAttribArray(self.position_location)

    def reset_color(self):
        self.colors = self.colors * np.uint8(255)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.cbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.colors.nbytes, self.colors)
        gl.glEnableVertexAttribArray(self.color_location)


    def update_empty():
        pass
        


    def run(self, update_function = update_empty):
        while not glfw.window_should_close(self.window):
            # Render here, e.g. using pyOpenGL
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            update_function()

            gl.glDrawElementsInstanced(gl.GL_TRIANGLES, self.square_indices.size, gl.GL_UNSIGNED_BYTE, None, self.max_square_num)

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()
        print("Done!")

    