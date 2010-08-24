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
    varying vec3 normal;
    void main() {
        normal = gl_NormalMatrix * gl_Normal;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    ''', '''
    // Fragment program
    varying vec3 normal;
    void main() {
        float intensity;
        vec4 color;
        vec3 n = normalize(normal);
        vec3 l = normalize(gl_LightSource[0].position).xyz;
 
        // quantize to 5 steps (0, .25, .5, .75 and 1)
        intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;
        color = vec4(intensity*1.0, intensity*0.5, intensity*0.5,
            intensity*1.0);
 
        gl_FragColor = color;
    }
    ''')
 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, width/float(height), 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    
    quit = False
    angle = 0
    angle_increasing = True
    while not quit:
        for e in pygame.event.get():
            if e.type in (QUIT, KEYDOWN):
                quit = True
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslate(0.0, 0.0, -2.5)
        glRotate(angle, 0.0, 0.0, -5.0)
        glUseProgram(program)
        glutSolidTeapot(0.5)
        
        if angle < 25 and angle_increasing:
            angle += 0.5
        else:
            if angle_increasing:
                angle_increasing = False
            angle -= 0.5
            if angle < -25:
                angle_increasing = True
            
        pygame.display.flip()
