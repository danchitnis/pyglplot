import glfw
from OpenGL import GL as gl
import numpy as np
import time


lineSize = 2000

lineNum = 200

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
    outColor = vec4(vColor,0.8);
}
"""

if not glfw.init():
    exit()
# Create a windowed mode window and its OpenGL context
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 1)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)

glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)  # for windows
#glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.EGL_CONTEXT_API) # for linux
#glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.OSMESA_CONTEXT_API)


window = glfw.create_window(1280, 800, "pyglplot", None, None)
if not window:
    glfw.terminate()
    exit()
# Make the window's context current
glfw.make_context_current(window)
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

program = gl.glCreateProgram()
gl.glAttachShader(program, vertex_shader)
gl.glAttachShader(program, fragment_shader)
gl.glLinkProgram(program)


color_buffer = np.zeros( lineSize * lineNum * 3, dtype=np.uint8)

cbo = gl.glGenBuffers(1)

gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cbo)
gl.glBufferData(gl.GL_ARRAY_BUFFER, color_buffer.nbytes, color_buffer, gl.GL_STATIC_DRAW)

colorLocation = gl.glGetAttribLocation(program, "a_color")
gl.glVertexAttribPointer(colorLocation, 3, gl.GL_UNSIGNED_BYTE, gl.GL_FALSE, 0, None)
gl.glEnableVertexAttribArray(colorLocation)


vertex_buffer = np.zeros( lineSize * lineNum * 2, dtype=np.float32)


vbo = gl.glGenBuffers(1)

gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
gl.glBufferData(gl.GL_ARRAY_BUFFER, vertex_buffer.nbytes, vertex_buffer, gl.GL_DYNAMIC_DRAW)

positionLocation = gl.glGetAttribLocation(program, "a_position")
gl.glVertexAttribPointer(positionLocation, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
gl.glEnableVertexAttribArray(positionLocation)


gl.glUseProgram(program)

gl.glClearColor(0.1, 0.1, 0.1, 1.0)




def on_resize(window, width, height):
    gl.glViewport(0, 0, width, height)



def updateColor():
    color_buffer = np.zeros( lineSize * lineNum * 3, dtype=np.uint8)

    # each line has a different random color
    for i in range(lineNum):
        r = np.random.randint(0, 255)
        g = np.random.randint(0, 255)
        b = np.random.randint(0, 255)

        color_buffer[i * lineSize * 3 : (i + 1) * lineSize * 3] = np.concatenate((np.tile([r, g, b], lineSize),))
    
    
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cbo)

    gl.glBufferData(gl.GL_ARRAY_BUFFER, color_buffer.nbytes, color_buffer, gl.GL_STATIC_DRAW)

    gl.glEnableVertexAttribArray(colorLocation)


updateColor()

glfw.set_window_size_callback(window, on_resize)


data = np.zeros(lineSize * 2, dtype=np.float32)

data[0::2] = np.linspace(-1, 1, lineSize)



def updateLines():

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

    phase = glfw.get_time() * 0.1

    y0 = np.linspace(0, 1, lineNum) + phase

    for i in range(lineNum):
        y = y0[i] + np.linspace(0, 1, lineSize) * 0.1
        yy = np.mod(y, 1) * 2 - 1

        data[1::2] = yy

        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, i * lineSize * 2 * 4, data.nbytes, data)


    gl.glEnableVertexAttribArray(positionLocation)


elasped_time = 0
frame_count = 0

while not glfw.window_should_close(window):
    # Render here, e.g. using pyOpenGL
    
    start_time = time.perf_counter_ns()


    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    updateLines()

    for i in range(lineNum):
        gl.glDrawArrays(gl.GL_LINE_STRIP, i * lineSize, lineSize)


    # Swap front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

    end_time = time.perf_counter_ns()

    elasped_time += end_time - start_time

    frame_count += 1

    if elasped_time > 1e9:
        print("FPS: ", frame_count)
        frame_count = 0
        elasped_time = 0

glfw.terminate()
print("Done!")

    