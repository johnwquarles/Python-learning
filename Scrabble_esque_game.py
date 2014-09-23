# Notes from John: 
# 
# This game was constructed function by function as part of a problem set for MIT's 6.00.1x course on edx.org.
# The problem's authors gave instructions as to what each function is supposed to do (as can be seen in the comments), while 
# the student (in this case, me, John) codes each function.
# The initial Helper code, and the functions displayHand and dealHand
# were provided by the authors.
# 
# Upon completing the problem set, I changed the formatting just a bit and made the game prompt 
# the user for his/her desired hand size prior to each game
# (wanted to play around with making the computer play hands of 900+ letters)
# (which was everything I imagined it could be)
#
# In the game, a set of user-determined size random letters is presented. The user can make words out of them (each letter
# can only be used once) for points according to scrabble letter point values; the point total for each letter is added and
# multiplied by the number of letters in the word.
#
# If the user (or computer) can use every letter on the very first try, there's a fifty-point bonus.
# The user can try for him/herself or have the computer play.
#
# /end notes from John
#
# 6.00x Problem Set 4A Template
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
# Modified by: Sarina Canelake <sarina>
#

import random
import string
import time

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7                                          # default hand size; set up to be changed by user upon opening game

# the below dictionary determines individual letter values
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------
#
# Problem #1: Scoring a word
#

def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    x = 0
    y = 0
    if ((turn == 0) and (len(word) == n)):   #check for initial turn/all letter bonus
        for i in word:
            x += SCRABBLE_LETTER_VALUES[i]   # Add Scrabble letter points for each letter
        y = (x * len(word)) + 50             # And multiply by the amount of letters, and add the bonus.
        return y
    else:
        for i in word:
            x += SCRABBLE_LETTER_VALUES[i]
        y = x * len(word)
        return y
        
#
# Problem #2: Make sure you understand how this function works and what it does!
#

def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

#
# Problem #2: Make sure you understand how this function works and what it does!
#

def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n / 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand
    
#
# Problem #2: Update a hand by removing letters
#

def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    newHand = hand.copy()                         # make a copy of the current hand
    for i in word:                                # for each letter in the word
        newHand[i] -= 1                           # delete one copy from the new hand
        if newHand[i] <= 0:                       # if this makes any letter amounts go to zero
            del newHand[i]                        # delete them from the dictionary that comprises the new hand
    return newHand                                # return the new hand

#
# Problem #3: Test word validity
#

def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    if (word in wordList) != True:                           # if the user's word isn't in the list
        return False                                         # then the word isn't valid.
    else:
        amt = getFrequencyDict(word)                         # otherwise, make a dictionary of its letters (keys) and amounts (values)
        for i in word:
            if amt.get(i, 0) > hand.get(i, 0):               # but then if the word contains any letters that aren't in the hand
                return False                                 # or the user is trying to use more of a certain letter than
        return True                                          # is in the hand, the word isn't valid.
        
#
# Problem #4: Playing a hand
#

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(hand.values())

def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    score = 0                                                   # start with a score of zero; add to this integer as we go.
    global turn                                              # need turn to be available outside of this function
    turn = 0                                                  # just started; no turns elapsed yet.
    while calculateHandlen(hand) > 0:                           # continue playing while there are still letters left in hand
        print ""
        print "Current Hand: ",
        displayHand(hand)
        print ""
        word = raw_input("Enter word, or a \".\" to indicate that you are finished: ")          # display hand, enter "." to finish
        if word == "." :
            break
        else:
            if isValidWord(word, hand, wordList) != True:                     # run in case of invalid word input.
                print ""
                print "No good! That's either not a word, or you don't have the letters to make it.\n"
            else:
                print ""
                print word,
                print "earned ",
                print getWordScore(word, n),
                print "points.",
                score += getWordScore(word, n)                              # keep running total of score
                print "Total: %i points\n" % score                          # print everything out for the user
                hand = updateHand(hand, word)                               # use this function to make the new hand
                turn += 1                                               # no bonus chance anymore; a turn has elapsed
    print ""
    print "Total score: " + str(score) + " points."                 # this is run upon exiting the loop, i.e when there are no letters left
                                                                    # or the user enters "." to quit playing on a particular hand.
#
#
# Problem #6: Computer chooses a word
#         (problem #5 is extraneous for this particular version of the game)
#

def compChooseWord(hand, wordList, n):                     # n is hand size
    """
    Given a hand and a wordList, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)

    returns: string or None
    """
    
    topScore = 0                                   # start at zero; best score that computer can make on a particular turn is stored here
    topWord = None                                 # and the word that gets it that score is stored here
    for i in wordList:                             # goes through every word in the wordList
        if compValidWord(i, hand) == True:          # and for each word that would be a valid play given the computer's hand, 
            wordScore = getWordScore(i, n)          # we see how many points it'd be worth
            if wordScore > topScore:           # and if it's worth more than the best scoring opportunity we've found thus far,
                topScore = wordScore           # naturally, *it* is the best scoring opportunity we've found thus far.
                topWord = i                    # so we copy its score value and the word itself
    return topWord                             # and return the word. If there's no scoring to be had, topScore is 0 and topWord is None.

def compValidWord(word, hand):                # using the isValidWord function for the computer made an infinite loop, so it is
    amt = getFrequencyDict(word)              # is rewritten and simplified here; don't need to make sure that each
    for i in word:                            # word is in the wordList since computer is only pulling from the wordList in the first place.
        if amt.get(i, 0) > hand.get(i, 0):
            return False        
    return True
    
#
# Problem #7: Computer plays a hand
#

def compPlayHand(hand, wordList, n):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).
 
    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """
    global turn                                               # need turn to be available outside of this function
    turn = 0                                                  # check for whether or not we're on the first turn for bonus awarding purposes
    compScore = 0                                                         # keep track of computer's running total score
    while compChooseWord(hand, wordList, n) != None:                      # so long as there's scoring to be had by the computer,
        
        print ""
        print "Current Hand: ",
        displayHand(hand)
        print ""                                                          # show its hand,
        compChoice = compChooseWord(hand, wordList, n)                    # get its choice for a scoring play,
        print "\"" + compChoice + "\"",                                   # show what it is, surrounded by quotes,
        print "earned ",
        print getWordScore(compChoice, n),
        print "points.",                                                  # show how many points the computer got,
        compScore += getWordScore(compChoice, n)                          # add that to its running total score
        print "Total: %i points\n" % compScore                            # and show what that is, too
        hand = updateHand(hand, compChoice)                               # subtract the used letters from its hand
        turn += 1                                               # bonus chance is no more
        
    if calculateHandlen(hand) != 0:                         # If the computer still has letters in its hand,                              
        print ""
        print "Current Hand: ",                              # show them
        displayHand(hand)
         
    print ""
    print "Total score: " + str(compScore) + " points."         # and finally, upon exiting the loops (computer has no more scoring plays),
                                                                # show the computer's total score.
# Problem #8: Playing a game
#
#

def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.
      
        * If the user inputted 'u', let the user play the game
          with the selected hand, using playHand.
        * If the user inputted 'c', let the computer play the 
          game with the selected hand, using compPlayHand.

    4) After the computer or user has played the hand, repeat from step 1

    wordList: list (string)"""
    
    while True:                                                             # loop until there's a satisfactory answer from the user
        print ""
        choice = raw_input("How many letters in a hand? ")
        try:
            HAND_SIZE = int(choice)                                         # if the user gives an integer, store it and move on.
            break
        except ValueError:                                                  # or if user's answer results in a ValueError (isn't an integer),
            print ""
            print "what?"                                                   # express confusion and ask again.
    
    while True:                                                             # loop until broken deliberately
        print ""
        choice = raw_input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ")
        if choice == "n":
            while True:                                                     # loop until broken deliberately
                print ""
                who = raw_input("Enter u to have yourself play, c to have the computer play: ")
                if who == "u":
                    hand = dealHand(HAND_SIZE)                              # deal a new hand
                    print ""
                    playHand(hand, wordList, HAND_SIZE)                     # start the game for the user
                    break                                                   # and upon completion, break out of comp/human loop, and go back to new/same/exit game loop
                elif who == "c":
                    hand = dealHand(HAND_SIZE)                              # deal a new hand
                    print ""
                    compPlayHand(hand, wordList, HAND_SIZE)                 # start the game for the computer
                    break                                                   # and upon completion, break out of comp/human loop, and go back to new/same/exit game loop
                else:
                    print ""
                    print "Invalid command."                                # if the answer is no good, loop until we get one that is.
        elif choice == "r":
            while True:
                print ""
                try:
                    hand == 0                                                   # do this to bring up a NameError if the user requests the same hand despite not having been dealt a hand yet, so that we get the exception prior to entering the comp/human loop.
                    who = raw_input("Enter u to have yourself play, c to have the computer play: ")
                    if who == "u":                    
                        print ""
                        playHand(hand, wordList, HAND_SIZE)
                        break
                    elif who == "c":                    
                        print ""
                        compPlayHand(hand, wordList, HAND_SIZE)
                        break
                    else:
                        print ""
                        print "Invalid command."
                except NameError:                                               # deal with the NameError that will be raised if the user requests the same hand despite not having been dealt a hand yet.
                    print "You have not played a hand yet. Please play a new hand first!"  #print this and break back to the new/same/exit question.
                    break
        elif choice == "e":
            break                                                           # all done
        else:
            print ""
            print "Invalid command."                                        # print this and re-ask question.
            
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
