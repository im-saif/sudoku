import pygame as pg


class Button:
    def __init__(self,x,y,width,height,text = None,color = (73,73,73),highlightedColor = (189,189,189),function = None, params = None ):
        self.image = pg.Surface((width,height))
        self.pos = (x,y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.color = color
        self.highlightedColor = highlightedColor
        self.function = function
        self.params = params
        self.highlighted = False
        self.width = width
        self.height = height

    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self,window):
        self.image.fill(self.highlightedColor if self.highlighted else self.color)
        if self.text:
            self.drawText(self.text)
        window.blit(self.image, self.pos)

    def click(self):
        if self.params:
            self.function(self.params)
        else:
            self.function()

    def drawText(self,text):
        font = pg.font.SysFont("arial",20,bold = 1)
        text = font.render(text,False,(0,0,0))
        width,height = text.get_size()
        x = (self.width-width)//2
        y = (self.height-height)//2
        self.image.blit(text, (x,y))