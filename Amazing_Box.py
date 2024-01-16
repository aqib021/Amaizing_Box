from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

W_Width, W_Height = 500, 500

points = []
speed = 1.0
freeze = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.random(), random.random(), random.random())
        self.direction = (random.choice([-1, 1]), random.choice([-1, 1]))
        self.blinking = False
        self.blink_time = time.time()
        self.blink_duration = 1.0

def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

def draw_point(p):
    glPointSize(5)
    glColor3f(p.color[0], p.color[1], p.color[2])
    glBegin(GL_POINTS)
    glVertex2f(p.x, p.y)
    glEnd()

def generate_random_movable_point(x, y):
    new_point = Point(x, y)
    points.append(new_point)

def adjust_speed(key):
    global speed
    if key == GLUT_KEY_UP:
        speed *= 1.5
    elif key == GLUT_KEY_DOWN:
        speed /= 1.5

def mouse_click(button, state, x, y):
    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            x, y = convert_coordinate(x, y)
            generate_random_movable_point(x, y)
        elif button == GLUT_LEFT_BUTTON:
            for point in points:
                point.blinking = not point.blinking
                point.blink_time = time.time()

def keyboard_listener(key, x, y):
    global freeze
    if key == b' ':
        freeze = not freeze

def animate():
    global points, speed, freeze
    if not freeze:
        for point in points:
            if not point.blinking:
                point.x += point.direction[0] * speed
                point.y += point.direction[1] * speed
                if point.x < -W_Width / 2 or point.x > W_Width / 2:
                    point.direction = (-point.direction[0], point.direction[1])
                if point.y < -W_Height / 2 or point.y > W_Height / 2:
                    point.direction = (point.direction[0], -point.direction[1])
            else:
                if time.time() - point.blink_time > point.blink_duration:
                    point.color = (random.random(), random.random(), random.random())
                    point.blink_time = time.time()
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W_Width / 2, W_Width / 2, -W_Height / 2, W_Height / 2, -1, 1)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    for point in points:
        draw_point(point)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(W_Width, W_Height)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Building the Amazing Box")
    init()
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_click)
    glutSpecialFunc(adjust_speed)
    glutKeyboardFunc(keyboard_listener)
    glutMainLoop()

if __name__ == "__main__":
    main()
