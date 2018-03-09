"""
This is a worked example of applying the Model-View-Controller (MVC)
design pattern to the creation of a simple arcade game (in this case
Brick Breaker).
We will create our game in stages so that you can see the process by
which the MVC pattern can be utilized to create clean, extensible,
and modular code.
@author: SoftDesProfs
"""

import pygame
import os
from pygame.locals import *
import time


def load_image(file_name, colorkey=False, image_directory='images'):
    """Loads an image, file_name, from image_directory, for use in pygame
        Borrowed from Pygames"""
    #file = os.path.join(image_directory, file_name)
    image_file = os.path.join(file_name)
    _image = pygame.image.load(image_file)
    if colorkey:
        if colorkey == -1:
        # If the color key is -1, set it to color of upper left corner
            colorkey = _image.get_at((0, 0))
        _image.set_colorkey(colorkey)
        _image = _image.convert()
    #else: # If there is no colorkey, preserve the image's alpha per pixel.
    #    _image = _image.convert_alpha()
    return _image

class PyGameWindowView(object):
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.image = load_image('boston.jpg')
        self.screen.blit(self.image, (0,0))
        pygame.display.update()

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(0,0,0))
        self.screen.blit(self.image, (0,0))

        for brick in self.model.bricks:
            pygame.draw.rect(self.screen,
                             pygame.Color(255, 255, 255),
                             pygame.Rect(brick.x,
                                         brick.y,
                                         brick.width,
                                         brick.height))
        pygame.draw.rect(self.screen,
                         pygame.Color(255, 0, 0),
                         pygame.Rect(self.model.paddle.x,
                                     self.model.paddle.y,
                                     self.model.paddle.width,
                                     self.model.paddle.height))
        pygame.display.update()

class ButtonModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.bricks = []
        self.numBricks = 4
        self.brick_width = 96
        self.brick_height = 20
        self.brick_space = 5
        for x in range(1,self.numBricks*(self.brick_space + self.brick_width),
                       self.brick_width + self.brick_space):
            self.bricks.append(Brick(self.brick_height,
                                     self.brick_width,
                                     x,
                                     350))
        self.paddle = Paddle(5, 5, 200, 300)

    def update(self):
        """ Update the game state (currently only tracking the paddle) """
        self.paddle.update()

    def __str__(self):
        output_lines = []
        # convert each brick to a string for outputting \|\|\|\|\\
        for brick in self.bricks:
            output_lines.append(str(brick))
        output_lines.append(str(self.paddle))
        # print one item per line
        return "\n".join(output_lines)

class Brick(object):
    """ Encodes the state of a brick in the game """
    def __init__(self,height,width,x,y):
        self.height = height
        self.width = width
        self.color = 'white'
        self.x = x
        self.y = y

    def __str__(self):
        return "Brick height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y)
  def update(self):
      self.color = 'blue'
class Paddle(object):
    """ Encodes the state of the paddle in the game """
    def __init__(self, height, width, x, y):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = 0.0

    def update(self):
        """ update the state of the paddle """
        self.x += self.vx

    def __str__(self):
        return "Paddle height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                           self.y)

class PyGameMouseController(object):
    """ A controller that uses the mouse to move the paddle """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Handle the mouse event so the paddle tracks the mouse position """
        if event.type == MOUSEMOTION:
            self.model.paddle.x = event.pos[0] - self.model.paddle.width/2.0
            self.model.paddle.y = event.pos[1] - self.model.paddle.height/2.0

class PyGameKeyboardController(object):
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Left and right presses modify the x velocity of the paddle """
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle.vx += -1.0
        if event.key == pygame.K_RIGHT:
            self.model.paddle.vx += 1.0

if __name__ == '__main__':
    pygame.init()

    size = (640, 480)
    model = ButtonModel(size)
    #print(model)
    #pygame.Surface()
    view = PyGameWindowView(model, size)
    #controller = PyGameKeyboardController(model)
    controller = PyGameMouseController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.01)
    pygame.quit()
