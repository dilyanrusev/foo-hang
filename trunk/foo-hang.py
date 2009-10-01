import random

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
	

if __name__ == "__main__":
	words = loadWords()
	print getRandomWord(words)
