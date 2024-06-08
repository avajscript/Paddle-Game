import pygame as pg
class Button(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False
        screen.blit(self.image, self.rect)
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False


        return action

