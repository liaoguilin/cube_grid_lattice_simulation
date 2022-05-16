# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
from glumpy.transforms import *
from glumpy import app, gl, glm, gloo
from glumpy.geometry import colorcube
from auxl.three_d_object_base import *
vertex = """
uniform mat4   u_model;         // Model matrix
uniform mat4   u_view;          // View matrix
uniform mat4   u_projection;    // Projection matrix
attribute vec3 a_position;      // Vertex position
void main()
{
    gl_PointSize = 3.0;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    gl_Position = <transform>;
}
"""

fragment = """
void main()
{
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

@window.event
def on_draw(dt):
    global phi, theta
    window.clear()
    entity.update_grid()
    cube["a_position"]=entity.obj.reshape(1331,3)
    # cube["a_position"]=entity.obj

    # Filled cube
    cube.draw(gl.GL_POINTS, I)
    # Make cube rotate
    theta += 0.5 # degrees
    phi += 0.5 # degrees
    model = np.eye(4, dtype=np.float32)
    # glm.rotate(model, theta, 0, 0, 1)
    # glm.rotate(model, phi, 0, 1, 0)
    cube['u_model'] = model


@window.event
def on_resize(width, height):
    cube['u_projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

entity=Cube(11,11,11,0.1,0.0000005,0.000001)

V = np.zeros((11,11,11), [("a_position", np.float32, 3)])
"""default"""
# V["a_position"] = [[ 1, 1, 9], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
#                    [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
"""modified"""
V["a_position"]=entity.obj
V = V.view(gloo.VertexBuffer)
"""default"""
# I = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
#               1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)
"""modified"""
I=np.arange(3993).astype(np.uint32)
I = I.view(gloo.IndexBuffer)

cube = gloo.Program(vertex, fragment)
cube.bind(V)
cube['transform'] = Trackball(Position("a_position"))
window.attach(cube["transform"])
# cube['u_model'] = np.eye(4, dtype=np.float32)
cube['u_view'] = glm.translation(-0.5, -0.5, -5)
phi, theta = 40, 30
gl.glEnable(gl.GL_POINT_SMOOTH)
gl.glEnable(gl.GL_DEPTH_TEST)


app.run()
