import pygame as pg
import math
import sys
from pygame.locals import *
from button import Button


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
MAX_PADDLE_MOVE_SPEED = 10
BALL_MOVE_SPEED = 6
PADDLE_VELOCITY_ITERATION_MS = 50



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


# Screen text elements


# Screen information
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

MID_SCREEN_HORIZONTAL = SCREEN_WIDTH / 2
MID_SCREEN_VERTICAL = SCREEN_HEIGHT / 2

DISPLAYSURF = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# load  images
resume_button_image = pg.image.load("assets/resume_button.png").convert_alpha()
paddle_one_img = pg.image.load("assets/glasspaddle2.png")
paddle_one_img = pg.transform.scale(paddle_one_img, (32, 128))
paddle_two_img = pg.image.load("assets/paddle.png")
paddle_two_img = pg.transform.scale(paddle_two_img, (32, 128))
ball_img = pg.image.load("assets/ball.png")
ball_img = pg.transform.scale(ball_img, (32, 32))

# create button instances
resume_button = Button(resume_button_image, MID_SCREEN_HORIZONTAL, MID_SCREEN_VERTICAL)


# Game state
running = True
paused = False
resetting = False

pg.display.set_caption("Game")

class Paddle(pg.sprite.Sprite):
    def __init__(self, image, x, y,  up_key, down_key, velocity, max_velocity):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.min_velocity = velocity
        self.velocity = velocity
        self.max_velocity = max_velocity
        self.up_pressed = False
        self.down_pressed = False
        self.start_ticks = 0
        self.up_key = up_key
        self.down_key = down_key
        self.direction = ""
    def update(self):
        pressed_keys = pg.key.get_pressed()

        # up key is pressed, so move paddle up
        if pressed_keys[self.up_key]:
            self.direction = "up"
            # key isn't pressed, so set the pressed state and reset the start time
            if not self.up_pressed:
                self.up_pressed = True
                self.start_ticks = pg.time.get_ticks()
            else:
                # key is pressed so increase the timer
                ms = pg.time.get_ticks() - self.start_ticks
                self.velocity = min((math.floor(ms / PADDLE_VELOCITY_ITERATION_MS) + self.min_velocity),
                                    self.max_velocity)
            # move up if below top of screen
            if self.rect.y > 0:
                self.rect.move_ip(0, -self.velocity)
        # up key isn't pressed, remove the pressed state and reduce the velocity
        else:
            if self.up_pressed:
                self.up_pressed = False
                self.start_ticks = pg.time.get_ticks()
            if self.velocity > self.min_velocity:
                ms = pg.time.get_ticks() - self.start_ticks
                self.velocity = max((self.max_velocity - math.floor((ms / PADDLE_VELOCITY_ITERATION_MS)),
                                     self.min_velocity))

        # down key is pressed, so move paddle down
        if pressed_keys[self.down_key]:
            self.direction = "down"
            # key isn't pressed, so set the pressed state and reset the start time
            if not self.down_pressed:
                self.down_pressed = True
                self.start_ticks = pg.time.get_ticks()
            if self.velocity > self.min_velocity:
                self.start_ticks -= (self.velocity - self.min_velocity) * PADDLE_VELOCITY_ITERATION_MS

            else:
                # key is pressed so increase the timer
                ms = pg.time.get_ticks() - self.start_ticks
                self.velocity = min((math.floor(ms / PADDLE_VELOCITY_ITERATION_MS) + self.min_velocity),
                                    self.max_velocity)

            if (self.rect.y + self.rect.height) < SCREEN_HEIGHT:
                self.rect.move_ip(0, self.velocity)
        else:
            if self.down_pressed:
                self.down_pressed = False
                self.start_ticks = pg.time.get_ticks()
            if self.velocity > self.min_velocity:
                ms = pg.time.get_ticks() - self.start_ticks
                self.velocity = max((self.max_velocity - math.floor((ms / PADDLE_VELOCITY_ITERATION_MS)),
                                     self.min_velocity))

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class Ball(pg.sprite.Sprite):
    def __init__(self, image, x, y, xDir, yDir):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.length = self.image.get_width()
        self.rect.x = x
        self.rect.y = y
        self.xDir = xDir
        self.yDir = yDir
        self.yDirOffset = 1
    def update(self):
        x = 0
        y = 0
        if self.xDir == "right":
            x = BALL_MOVE_SPEED
            if self.rect.x + x + self.length > SCREEN_WIDTH:
                self.xDir = "left"
                score["playerOne"] += 1
                self.reset()
        elif self.xDir == "left":
            x = -BALL_MOVE_SPEED
            if self.rect.x - x < 0:
                self.xDir = "right"
                score["playerTwo"] += 1
                self.reset()
        if self.yDir == "up":
            y = -BALL_MOVE_SPEED
            if self.rect.y - y < 0:
                self.yDir = "down"
        elif self.yDir == "down":
            y = BALL_MOVE_SPEED
            if self.rect.y + y + self.length > SCREEN_HEIGHT:
                self.yDir = "up"

        self.rect.move_ip(x, y * self.yDirOffset)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def bounce(self, paddleDirection, paddleVelocity):
        offset = paddleVelocity / 20
        if paddleDirection == "up":
            self.yDirOffset -= offset
        else:
            self.yDirOffset += offset

        self.yDirOffset = self.yDirOffset
        if self.xDir == "left":
            self.xDir = "right"
        elif self.xDir == "right":
            self.xDir = "left"

    def reset(self):
        self.rect.center = (MID_SCREEN_HORIZONTAL, MID_SCREEN_VERTICAL)
        global resetting
        resetting = True


P1 = Paddle(paddle_one_img, 20, 20, K_w, K_s, PADDLE_MOVE_SPEED, MAX_PADDLE_MOVE_SPEED)
P2 = Paddle(paddle_two_img, SCREEN_WIDTH - 20 - PADDLE_WIDTH, 20, K_UP, K_DOWN,
            PADDLE_MOVE_SPEED, MAX_PADDLE_MOVE_SPEED)
ball = Ball(ball_img, MID_SCREEN_HORIZONTAL, MID_SCREEN_VERTICAL, "right", "down")

paddles = [P1, P2]
def collideAny(sprite, rect_list):
    for rect in rect_list:
        if pg.sprite.collide_rect(sprite, rect):
            return rect
    return False



while running:
    # draw the background no matter what
    DISPLAYSURF.fill(BACKGROUND_COLOR)

    if paused:
        if resume_button.draw(DISPLAYSURF):
            paused = False


    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if resetting:
                resetting = False
            if event.key == pg.K_SPACE:
                paused = True
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    if not paused:
        # update the sprite positions
        if not resetting:
            P1.update()
            P2.update()
            ball.update()

        # draw the sprites

        P1.draw(DISPLAYSURF)
        P2.draw(DISPLAYSURF)
        ball.draw(DISPLAYSURF)

        # check if ball hit any paddles
        paddle = collideAny(ball, paddles)
        if paddle:
            ball.bounce(paddle.direction, paddle.velocity)

        # update text elements based on current score
        score_text = font.render(f'Player one: {score["playerOne"]}, Player two: {score["playerTwo"]}', True,
                                 PADDLE_COLOR)
        press_space_text = font.render(f'Press spacebar to pause the game', True, PADDLE_COLOR)

        # draw text elements
        DISPLAYSURF.blit(score_text, (MID_SCREEN_HORIZONTAL - (score_text.get_width() / 2), 10))
        DISPLAYSURF.blit(press_space_text, (MID_SCREEN_HORIZONTAL - (press_space_text.get_width() / 2),
                                            SCREEN_HEIGHT - press_space_text.get_height() - 20))



    # update the screen on 60 fps basis
    pg.display.update()
    FramePerSec.tick(FPS)