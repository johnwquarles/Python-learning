# This is a traditional hangman game made for an online course.
# The code toward the top was provided.
# I wrote the code below "# end of helper code" with conceptual guidance from the problem set.
# This game depends on a "words.txt" file
# that it randomly draws its secret word from
# for each game (the word that the player is guessing).

import random
import string

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# I (John) wrote the code below this point.

def isWordGuessed(secretWord, lettersGuessed):
	for x in range(0, len(secretWord)):
		letter = secretWord[x]
		if (letter in lettersGuessed) == False:
			return False
	return True


def getGuessedWord(secretWord, lettersGuessed):
	result = ""
	for x in range(0, len(secretWord)):
		if (secretWord[x] in lettersGuessed) == True:
			result += secretWord[x]
		else:
			result += "_ "
	return result


def getAvailableLetters(lettersGuessed):
	avail = ""
	import string
	for x in range(0, len(string.ascii_lowercase)):
		if (string.ascii_lowercase[x] in lettersGuessed) == False:
			avail += string.ascii_lowercase[x]
	return avail

def hangman(secretWord):
	print "Welcome to the game Hangman!"
	print "I am thinking of a word that is %s letters long." % len(secretWord)
	print "------------"
	lettersGuessed = []
	mistakesMade = 0
	while mistakesMade < 8:
		sameletter = 0
		print "You have %d guesses left." % (8 - mistakesMade)
		print "Available letters: %s" % getAvailableLetters(lettersGuessed)
		guess = raw_input("Please guess a letter: ").lower()
		if (guess in lettersGuessed) == True:
			print "Oops! You've already guessed that letter: %s" % getGuessedWord(secretWord, lettersGuessed)
			print "------------"
			sameletter = 1
		lettersGuessed.append(guess)
		good = 0
		for x in range(0, len(secretWord)):
			if (secretWord[x] == guess and sameletter != 1):
				print "Good guess: %s" % getGuessedWord(secretWord, lettersGuessed)
				print "------------"
				good = 1
				if isWordGuessed(secretWord, lettersGuessed) == True:
					print "Congratulations, you won!"
					return True
				break
		if (good == 0 and sameletter != 1):
			mistakesMade += 1
			print "Oops! That letter is not in my word: %s" % getGuessedWord(secretWord, lettersGuessed)
			print "------------"
	print "Sorry, you ran out of guesses. The word was %s ." % secretWord
				
secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
