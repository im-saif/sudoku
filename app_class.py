import pygame as pg 
import sys
import requests
from bs4 import BeautifulSoup
from settings import *
from buttonClass import *
from random import randint

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Sudoku by Saif")
        self.window = pg.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.grid = easyBoard
        self.selected = None
        self.mousePos = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.playingButtons = []
        self.lockedCells = []
        self.incorrectCells = []
        self.font = pg.font.SysFont("arial", cellSize//2)
        self.grid = easyBoard
        self.load()
        
        
    
    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pg.quit()
        sys.exit()

    #PLAYER STATS FUNCTIONS

    def playing_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            # USER CLICKS
            if event.type == pg.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playingButtons:
                        if button.highlighted:
                            button.click()
            
            #USER TYPES A KEY
            if event.type == pg.KEYDOWN:
                if self.selected != None and self.selected not in self.lockedCells:
                    if self.isInt(event.unicode):
                        #cell changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChanged = True

    def playing_update(self):
        self.mousePos = pg.mouse.get_pos()  
        for button in self.playingButtons:
            button.update(self.mousePos)
        if self.cellChanged:
            self.incorrectCells = []

            if self.allCellsDone():
                #check if board is correct
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    self.finished = True



    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)

        if self.selected:
            self.drawSelection(self.window,self.selected)
        
        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeIncorrectCells(self.window, self.incorrectCells)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)
        pg.display.update()
        self.cellChanged = False
    

    #BOARD CHECKING FUNCTIONS
    def allCellsDone(self):
        for row in self.grid:
            for num in row:
                if num == 0:
                    return False
        return True

    def checkAllCells(self):
        self.checkRows()
        self.checkCols()
        self.checkSmallGrid()
        if self.checkRows() and self.checkCols and self.checkSmallGrid:
            self.textToScreen(self.window,"You Win",(50,-300))

    def checkSmallGrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1,2,3,4,5,6,7,8,9]
                
                for i in range(3):
                    for j in range(3):
                        xidx = x*3+i
                        yidx = y*3+j
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                                self.incorrectCells.append([xidx,yidx])
                            if [xidx,yidx] in self.lockedCells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x*3+k
                                        yidx2 = y*3+l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and ([xidx2,yidx2]) not in self.lockedCells:
                                            self.incorrectCells.append([xidx2,yidx2])



    def checkRows(self):
        for yidx, row in enumerate(self.grid):
            possibles = [1,2,3,4,5,6,7,8,9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx,yidx] not in self.lockedCells and [xidx,yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx,yidx])
                    if [xidx,yidx] in self.lockedCells:
                        for k in range(9):
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k,yidx] not in self.lockedCells:
                                self.incorrectCells.append([k, yidx])
    def checkCols(self):
        for xidx in range(9):
            possibles = [1,2,3,4,5,6,7,8,9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx,yidx] not in self.lockedCells and [xidx,yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx,yidx])
                    if [xidx,yidx] in self.lockedCells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx,k] not in self.lockedCells:
                                self.incorrectCells.append([xidx,k])



    #HELPER FUNCTIONS
    def easy(self):
        self.grid = randint(1,2)
        if self.grid == 1:
            self.grid = easyBoard
        else:
            self.grid = easyBoard2

    def medium(self):
        self.grid = randint(1,2)
        if self.grid == 1:
            self.grid = mediumBoard
        else:
            self.grid = mediumBoard2
    
    def hard(self):
        self.grid = randint(1,2)
        if self.grid == 1:
            self.grid = hardBoard
        else:
            self.grid = hardBoard2
    
    def supers(self):
        self.grid = randint(1,2)
        if self.grid == 1:
            self.grid = superBoard
        else:
            self.grid = superBoard2

    def quit(self):
        py.QUIT()


    def shadeLockedCells(self,window, locked):
        for cell in locked:
            pg.draw.rect(window, LOCKEDCELLCOLOR, (cell[0]*cellSize+gridPos[0],cell[1]*cellSize+gridPos[1], cellSize, cellSize))


    def shadeIncorrectCells(self,window,incorrect):
        for cell in incorrect:
            pg.draw.rect(window, RED, (cell[0]*cellSize+gridPos[0],cell[1]*cellSize+gridPos[1], cellSize, cellSize))

    def drawNumbers(self,window):
        for yidx,row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = [(xidx*cellSize)+gridPos[0], (yidx*cellSize)+gridPos[1]]
                    self.textToScreen(window,str(num),pos)


    def drawSelection(self,window,pos):
        pg.draw.rect(window,LIGHTBLUE,((pos[0]*cellSize)+gridPos[0],(pos[1]*cellSize)+gridPos[1], cellSize, cellSize))

    
    def drawGrid(self,window):
        pg.draw.rect(window,BLACK,(gridPos[0],gridPos[1], WIDTH-150,HEIGHT-150),3)
        for x in range(9):
            
            pg.draw.line(window, BLACK,(gridPos[0]+(x*cellSize),gridPos[1]),(gridPos[0]+(x*cellSize),gridPos[1]+450),3 if x%3 == 0 else 1)
            pg.draw.line(window, BLACK,(gridPos[0],gridPos[1]+(x*cellSize)),(gridPos[0]+450,gridPos[1]+(x*cellSize)),3 if x%3 == 0 else 1)
    
    
    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0]+gridSize or self.mousePos[1]> gridPos[1]+gridSize:
            return False
        return ((self.mousePos[0]-gridPos[0])//cellSize, (self.mousePos[1]-gridPos[1])//cellSize)

    def loadButtons(self):
        self.playingButtons.append(Button(20,40,WIDTH//7,40, function=self.checkAllCells, color = (27,142,207), text='Check'))
        self.playingButtons.append(Button(140,40,WIDTH//7,40, function=self.easy, text = 'Easy', color=(117,172,112)))
        self.playingButtons.append(Button(WIDTH//2 - (WIDTH//7)//2, 40, WIDTH//7,40, function=self.medium,text="Medium",color=(204,197,110)))
        self.playingButtons.append(Button(380, 40, WIDTH//7, 40, function=self.hard, text= "Hard",color=(199,129,48)))
        self.playingButtons.append(Button(500,40,WIDTH//7,40, function=self.supers, text="SUPER",color=(207,68,68)))
        self.playingButtons.append(Button(20,-400,WIDTH//7,40, function=self.quit, color =(27,176,207) ,text="QUIT"))

    def textToScreen(self,window,text,pos):
        font = self.font.render(text,False,BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize-fontWidth)//2
        pos[1] += (cellSize-fontHeight)//2
        window.blit(font,pos)

    def load(self):
        self.playingButtons = []
        self.loadButtons()
        self.lockedCells = []
        self.incorrectCells = []
        self.finished = False

        #Setting locked cells from original board 
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate (row):
                if num != 0:
                    self.lockedCells.append([xidx,yidx])
        
    def isInt(self,string):
        try:
             int(string)
             return True
        except:
            return False

