import pygame as pg
import math
import sys
from pygame.locals import *

pg.init()
pg.font.init()
font = pg.font.Font(None, 24)

FPS = 60
FramePerSec = pg.time.Clock()

score = {
    "playerOne": 0,
    "playerTwo": 0
}

# Movement constants
PADDLE_MOVE_SPEED = 3
MAX_PADDLE_MOVE_SPEED = 6
BALL_MOVE_SPEED = 6
PADDLE_VELOCITY_ITERATION_MS = 200

# Size constants
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
BALL_LENGTH = 10

# Color constants

# dark purple background
BACKGROUND_COLOR = (55, 0, 56)
PADDLE_COLOR = (254, 224, 255)
BALL_COLOR = (254, 224, 255)


BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

MID_SCREEN_HORIZONTAL = SCREEN_WIDTH / 2
MID_SCREEN_VERTICAL = SCREEN_HEIGHT / 2

DISPLAYSURF = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pg.display.set_caption("Game")

class Paddle(pg.sprite.Sprite):
    def __init__(self, color, x, y, width, height, up_key, down_key, velocity, max_velocity):
        super().__init__()
        self.color = color
        self.rect = pg.Rect(x, y, width, height)
        self.min_velocity = velocity
        self.velocity = velocity
        self.max_velocity = max_velocity
        self.w_pressed = False
        self.s_pressed = False
        self.start_ticks = 0
        self.up_key = up_key
        self.down_key = down_key
    def update(self):
        pressed_keys = pg.key.get_pressed()

        if pressed_keys[self.up_key]:
            # key isn't pressed, so set the pressed state and reset the start time
            if not self.w_pressed:
                self.w_pressed = True
                self.start_ticks = pg.time.get_ticks()
            else:
                # key is pressed so increase the timer
                ms = pg.time.get_ticks() - self.start_ticks
                self.velocity = min((math.floor(ms / PADDLE_VELOCITY_ITERATION_MS) + self.min_velocity),
                                    self.max_velocity)

            if self.rect.y > 0:
                self.rect.move_ip(0, -self.velocity)
        else:
            if self.w_pressed:
                self.w_pressed = False
                self.start_ticks = pg.time.get_ticks()
            if self.velocity > self.min_velocity:
                ms = pg.time.get_ticks() - self.start_ticks
                self.velocity = max((self.max_velocity - math.floor((ms / PADDLE_VELOCITY_ITERATION_MS)),
                                     self.min_velocity))

        if pressed_keys[self.down_key]:
            # key isn't pressed, so set the pressed state and reset the start time
            if not self.s_pressed:
                self.s_pressed = True
                self.start_ticks = pg.time.get_ticks()
                if self.velocity > self.min_velocity:
                    self.start_ticks -= (self.velocity - self.min_velocity) * PADDLE_VELOCITY_ITERATION_MS
                else:
                    print("less than 3 velocity")
            else:
                # key is pressed so increase the timer
                ms = pg.time.get_ticks() - self.start_ticks
                self.velocity = min((math.floor(ms / PADDLE_VELOCITY_ITERATION_MS) + self.min_velocity),
                                    self.max_velocity)

            if (self.rect.y + self.rect.height) < SCREEN_HEIGHT:
                self.rect.move_ip(0, self.velocity)
        else:
            if self.s_pressed:
                self.s_pressed = False
                self.start_ticks = pg.time.get_ticks()
            if self.velocity > self.min_velocity:
                ms = pg.time.get_ticks() - self.start_ticks
                self.velocity = max((self.max_velocity - math.floor((ms / PADDLE_VELOCITY_ITERATION_MS)),
                                     self.min_velocity))

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)



class Ball(pg.sprite.Sprite):
    def __init__(self, color, x, y, length, xDir, yDir):
        super().__init__()
        self.color = color
        self.rect = pg.Rect(x, y, length, length)
        self.radius = length / 2
        self.xDir = xDir
        self.yDir = yDir
    def update(self):
        x = 0
        y = 0
        if self.xDir == "right":
            x = BALL_MOVE_SPEED
            if self.rect.x + x + self.radius > SCREEN_WIDTH:
                self.xDir = "left"
                score["playerOne"] += 1
        elif self.xDir == "left":
            x = -BALL_MOVE_SPEED
            if self.rect.x - x - self.radius < 0:
                self.xDir = "right"
                score["playerTwo"] += 1
        if self.yDir == "up":
            y = -BALL_MOVE_SPEED
            if self.rect.y - y - self.radius < 0:
                self.yDir = "down"
        elif self.yDir == "down":
            y = BALL_MOVE_SPEED
            if self.rect.y + y + self.radius > SCREEN_HEIGHT:
                self.yDir = "up"

        self.rect.move_ip(x, y)

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.rect.x, self.rect.y), self.radius)

    def bounce(self):
        if self.xDir == "left":
            self.xDir = "right"
        elif self.xDir == "right":
            self.xDir = "left"

running = True

P1 = Paddle(PADDLE_COLOR, 20, 20, PADDLE_WIDTH, PADDLE_HEIGHT, K_w, K_s, PADDLE_MOVE_SPEED, MAX_PADDLE_MOVE_SPEED)
P2 = Paddle(PADDLE_COLOR, SCREEN_WIDTH - 20 - PADDLE_WIDTH, 20, PADDLE_WIDTH, PADDLE_HEIGHT, K_UP, K_DOWN,
            PADDLE_MOVE_SPEED, MAX_PADDLE_MOVE_SPEED)
ball = Ball(BALL_COLOR, MID_SCREEN_HORIZONTAL, MID_SCREEN_VERTICAL, BALL_LENGTH, "right", "down")

paddles = [P1, P2]
def collideAny(sprite, rect_list):
    for rect in rect_list:
        if pg.sprite.collide_rect(sprite, rect):
            return True
    return False



while running:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    # update the sprite positions
    P1.update()
    P2.update()
    ball.update()

    # draw the background and sprites
    DISPLAYSURF.fill(BACKGROUND_COLOR)
    P1.draw(DISPLAYSURF)
    P2.draw(DISPLAYSURF)
    ball.draw(DISPLAYSURF)

    # check if ball hit any paddles
    if collideAny(ball, paddles):
        ball.bounce()

    score_text = font.render(f'Player one: {score["playerOne"]}, Player two: {score["playerTwo"]}', True, PADDLE_COLOR)
    DISPLAYSURF.blit(score_text, (MID_SCREEN_HORIZONTAL - (score_text.get_width() / 2), 10))
    # update the screen on 60 fps basis
    pg.display.update()
    FramePerSec.tick(FPS)