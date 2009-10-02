import random
import pygame
from pygame.locals import *

font = None

def loadWords():
    "Load a list of words that the user should try to guess"
    words = {}

    with open("words.txt") as f:
        for line in f:
            pair = line.strip().split(":")
            if len(pair) > 1:
                words[pair[0].strip()] = pair[1].strip()
            else:
                words[pair[0].strip()] = ""
    return words

def getRandomWord(words):
    "Get a random word from a dictionary of words"
    numberOfWords = len(words)

    indexOfRandomWord = random.randint(0, numberOfWords - 1)
    randomWord = words.keys()[indexOfRandomWord]
    return randomWord

def showWindow():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Foo-Hang")
    return screen

def loadFont():
    global font
    if font is None:
        font = pygame.font.Font("AgentOrange.ttf", 32)

def drawText(screen, x, y, text):
    global font
    loadFont()
    text = font.render(text, True, (255, 255, 255), (0,0,0))
    text = text.convert()
    text.set_colorkey((0,0,0))
    screen.blit(text, (x,y))

def runLoop(screen):
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True
        if not done:
            drawText(screen, 10, 10, "Hello, world!")
            pygame.display.flip()


if __name__ == "__main__":
    #words = loadWords()
    #print getRandomWord(words)
    screen = None
    try:
        screen = showWindow()
        runLoop(screen)
    finally:
        pygame.quit()
