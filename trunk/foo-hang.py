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
    randomWord = list(words.keys())[indexOfRandomWord]
    guessedWord = randomWord[0] + ("-" * (len(randomWord) - 2)) + randomWord[-1];
    return randomWord, guessedWord

def showWindow():
    "Show and initialize the Pygame window"
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Foo-Hang (Press Esc to quit)")
    return screen

def loadFont():
    "load the global font variable if it is not already loaded"
    global font
    if font is None:
        font = pygame.font.Font("AgentOrange.ttf", 21)

def drawText(screen, x, y, text):
    "print some text on the screen at position (x, y)"
    global font
    loadFont()
    text = font.render(text, True, (255, 255, 255), (0,0,0))
    text = text.convert()
    text.set_colorkey((0,0,0))
    screen.blit(text, (x,y))

def contains(l, value):
    "Checks if an item belongs to a list"
    for item in l:
        if item == value:
            return True
    return False

def replace(original, mask, value):
    for i in range(len(original)):
        if original[i] == value:
            mask = mask[:i] + original[i] + mask[i+1:]
    return mask        

def same(left, right):
    for i in range(len(left)):
        if left[i] != right[i]:
            return False
    return True

def runLoop(screen):
    "Run the main game loop"
    words = loadWords()
    loadFont()
    
    images = []
    for i in range(1,6):
        img = pygame.image.load("hang_{0}.png".format(i))
        img = img.convert()
        images.append(img)

    
    currentWord, guessedWord = getRandomWord(words)
    
    pressedKeys = []
    wrong = 0
    maxWrong = 5
    win = False
    lose = False
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                elif (win or lose) and event.key == K_SPACE:
                    currentWord, guessedWord = getRandomWord(words)
                    pressedKeys = []
                    wrong = 0
                    win = False
                    lose = False
                
                keyName = pygame.key.name(event.key)
                if not lose and len(keyName) == 1 and not contains(pressedKeys, keyName):
                    pressedKeys.append(keyName)
                    
                    if contains(currentWord, keyName):
                        guessedWord = replace(currentWord, guessedWord, keyName)
                        if same(currentWord, guessedWord):
                            win = True
                    else:
                        if wrong < maxWrong:
                            wrong += 1
                            
                        if wrong == maxWrong:
                            lose = True                    
                    
        if not done:
            screen.fill((0,0,0))
            
            offset = 20
            lineHeight = font.get_height() + 10

            if not lose:
                drawText(screen, offset, offset, guessedWord)
            else:
                drawText(screen, offset, offset, currentWord)
                
            if not win and not lose:
                drawText(screen, offset, offset + lineHeight * 2, "Pressed symbols:")
                drawText(screen, offset, offset + lineHeight * 3, ", ".join(pressedKeys))
                drawText(screen, offset, offset + lineHeight * 4, "Wrong: {0} out of {1}".format(wrong, maxWrong))
            else:
                if win:
                    drawText(screen, offset, offset + lineHeight * 2, "You have won!")
                elif lose:                    
                    drawText(screen, offset, offset + lineHeight * 2, "You have lost!")
                drawText(screen, offset, offset + lineHeight * 3, "Press space for the next word")
                
            
            if wrong > 0 and wrong <= maxWrong:
                screen.blit(images[wrong - 1], (offset , offset + lineHeight * 5))
                
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
