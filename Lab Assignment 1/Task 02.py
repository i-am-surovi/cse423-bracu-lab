from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Default Values
 ## Window Size
W_Width, W_Height = 500, 500
create_new = []
speed = 0.01
# To blink the point
flag = False
# To Handle Freezing points with Spacebar
pause = False

# To generate point's coordinate
def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x
    b = W_Height - y
    return (a, b)

# To Blink The point
def change_flag(currFlag):
    global flag
    if flag == True:
        flag = False
        print("Back to Unblinking State")
    elif flag == False:
        flag = True
        print("Back to Blinking State")
    glutPostRedisplay()

# Task 2 (i)

def mouseListener(button, state, x, y):
    global create_new, pause, flag
    if pause == False:
        if button == GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN:
                print(x, y)
                create_new.append({
                    'position': convert_coordinate(x, y),
                    'direction': (random.choice([-1, 1]), random.choice([-1, 1])),
                    'color': (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
                })
                print(create_new)
# Task 2 (iii)
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                flag = True
                # Blink the point for 1 second
                print("Blinking State")
                # (1s = 1000ms, timerfunction, false = 0 [parameter of timer function])
                glutTimerFunc(1000, change_flag, 0)
        glutPostRedisplay()

# Task 2 (ii)
def specialKeyListener(key, x, y):
    global speed, pause
    if pause == False:
        if key == GLUT_KEY_UP:
            speed *= 2
            print("Speed Increased")
        if key == GLUT_KEY_DOWN:
            speed /= 2
            print("Speed Decreased")
    glutPostRedisplay()

# Task 2 (iv)
def keyboardListener(key, x, y):
    global pause
    if key == b' ':
         ## To Freeze the points
        if pause == False:
            pause = True
            print("Freezed all the functions")
        ## To Unfreeze the points
        elif pause == True:
            pause = False
            print("Unfreezed all the functions")
    glutPostRedisplay()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global create_new, speed, flag
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(0.0, 0.0, 0.0)

    # call the draw methods here
    if len(create_new) > 0:
        for i in create_new:
            m, n = i['position']
            glPointSize(5.0)
            glBegin(GL_POINTS)
            if flag:
                glColor3f(0, 0, 0)
# Flag False means I have to generate points
            else:
                glColor3f(i['color'][0], i['color'][1], i['color'][2])
            glVertex2f(m, n)
            glEnd()
    glutSwapBuffers()


def animate():
    glutPostRedisplay()
    global create_new, speed, W_Width, W_Height, pause
    if pause == False:

        for point in create_new:
            x, y = point['position']
            dir_x, dir_y = point['direction']
        # Updating new point generation directions
            x = x + (dir_x * speed)
            y = y + (dir_y * speed)
        # Handling points direction for bouncing between the screen
            if x < 0 or x > W_Width:
                point['direction'] = (-dir_x, dir_y)
            if y < 0 or y > W_Height:
                point['direction'] = (dir_x, -dir_y)

            point['position'] = (x, y)


glutInit()
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Amazing Box")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()