from __future__ import division
import sys
import ctypes
import itertools
from random import randint

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Sierpinski carpet: d=2, b=3, A=[1] and m=1
# Menger sponge: d=3, b=3, A=[1] and m=1
k = 2 # number of iteration
d = 3 # dimension (2 or 3)
b = 3 # base
A = None # digits ot omit, [1, .., b-2] if A = None
m = 1 # max number of coordinates allowed a digit from A at a point

width, height = 800, 700 # default screen size
buffers = None
angle = 0

#-----OpenGl things-----#

def initGL():
    glClearDepth(1);
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def timer(value):
   glutPostRedisplay()
   glutTimerFunc(15, timer, 0)

def reshape(width, height):
    if (height == 0):
        height = 1
    aspect = width/height

    glViewport(0, 0, width, height)
 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, aspect, 0.1, 20.0)

def draw():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity()

    #scale = 7
    #glScalef(scale, scale, scale)
    glTranslatef(0, 0, -4)
    axis = (1, 1, 1)
    if d > 2:
        glRotatef(angle, *axis)
    fractal()
    glutSwapBuffers()
    angle = (angle + 1) % 360

def fractal():
    glPointSize(5)
    glEnableClientState(GL_VERTEX_ARRAY);
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0]);
    glVertexPointer(d, GL_FLOAT, 0, None);
    glDrawArrays(GL_POINTS, 0, len(vertices)//d)

    glBindBuffer(GL_ARRAY_BUFFER, buffers[1]);
    glVertexPointer(d, GL_FLOAT, 0, None);
    glDrawArrays(GL_LINES, 0, len(edges)//d)
    glDisableClientState(GL_VERTEX_ARRAY);

#-----Vertices and edges-----#

def get_vertices(k, d, b, m=1, A=None):
    '''
    Get the vertices of the k-th iteration of the Sierpinski
    fractal of dimension d, base b, allowing at most m coordinates
    to have a digit in A in the same position
    '''
    if not A:
        A = range(1, b-1)
    if d>3:
        raise NotImplementedError("3-dimensional is the limit. For now...")
    vts = {} #orig: scaled
    # go through points one by one checking if it's good
    lim = b**k
    points = itertools.product(*[range(lim) for _ in range(d)])
    for point in points:
        add = True
        p = point[:]
        while any(_ > 0 for _ in p):
            next_dig = map(lambda x: x % b, p)
            if len([_ for _ in next_dig if _ in A]) > m:
                add = False
                break
            p = map(lambda x: x // b, p)
        if add:
            vts[point] = map(lambda x: 2*x/(lim-1) - 1, point)
    return vts

def get_edges(vertices, d):
    '''
    Get edges in d dimensions
    '''
    def neighbours(vertex):
        '''
        Neighbouring vertices for rendering
        '''
        ns = []
        for i in range(d):
            n = list(v[:])
            n[i] += 1
            n = tuple(n)
            if n in vertices:
                ns.append(n)
        #print("new", vertex, ns)
        return ns

    edges = []
    for v in vertices:
        new = map(lambda x: [vertices[v], vertices[x]], neighbours(v))
        edges += sum(new, [])
    return edges

vertices = get_vertices(k, d, b, A=A, m=m)
edges = get_edges(vertices, d)
vertices = sum(list(vertices.values()), [])
edges = sum(edges, [])

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Sierpinski")
    glutDisplayFunc(draw)
    glutReshapeFunc(reshape)
    glutTimerFunc(0, timer, 0)
    initGL()

    # load all points to gpu for faster rendering
    global buffers
    buffers = glGenBuffers(2)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glBufferData(GL_ARRAY_BUFFER, 
            len(vertices)*4,
            (ctypes.c_float*len(vertices))(*vertices), 
            GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glBufferData(GL_ARRAY_BUFFER, 
            len(edges)*4,
            (ctypes.c_float*len(edges))(*edges), 
            GL_DYNAMIC_DRAW)
    glutMainLoop()

main()
