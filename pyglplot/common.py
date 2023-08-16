import platform
import glfw
from OpenGL import GL as gl



def detect_platform_context():
    system = platform.system()
    if system == "Windows":
        return "Windows", "native"
    elif system == "Linux":
        print("release=",platform.release())
        # Detect WSL1 or WSL2
        if "microsoft" and ("WSL2" or "WSL1" or "WSL") in platform.release():
            return "WSL", "egl"
        else:
            return "Native Linux", "native"
    elif system == "Darwin":
        return "MacOS", "native"
    else:
        return system, "Unknown"


def create_window(width = 1280, height = 800, title = "pyglplot", context_api = "auto") -> any:
    if not glfw.init():
        exit()
    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 1)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)

    if context_api == "auto":
        system, context_api = detect_platform_context()
        print("Detected platform: ", system)
        print("Using context API: ", context_api)
        
    if context_api == "native":
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
    elif context_api == "egl":
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.EGL_CONTEXT_API)
    elif context_api == "osmesa":
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.OSMESA_CONTEXT_API)


    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        exit()
    # Make the window's context current
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    print(glfw.get_version_string())
    print(gl.glGetString(gl.GL_VERSION))

    return window


def create_shaders(vertex_shader_text, fragment_shader_text) -> any:
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

    shader_program = gl.glCreateProgram()
    gl.glAttachShader(shader_program, vertex_shader)
    gl.glAttachShader(shader_program, fragment_shader)
    gl.glLinkProgram(shader_program)

    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    return shader_program