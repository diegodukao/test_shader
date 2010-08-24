import pygame
from pygame.locals import *

from shader import *

if __name__ == '__main__':
    glutInit(sys.argv)
    width, height = 640, 480
    pygame.init()
    pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
 
    program = compile_program('''
    // Vertex program
    varying vec3 pos;
    void main() {
        pos = gl_Vertex.xyz;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    ''', '''
    // Fragment program
    varying vec3 pos;
    void main() {
        gl_FragColor.rgb = pos.xyz;
    }
    ''')
 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, width/float(height), 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    
    quit = False
    angle = 0
    while not quit:
        for e in pygame.event.get():
            if e.type in (QUIT, KEYDOWN):
                quit = True
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslate(0.0, 0.0, -2.5)
        glRotate(angle, 0.0, 0.0, -5.0)
        glUseProgram(program)
        glutSolidTeapot(1.0)
        angle += 0.1 
        pygame.display.flip()
