from utils import rectangle, word_rectangle_pair


def wordToSentence(paragraph, i, j, wordRectanglePairArray):

    prevLine = wordRectanglePairArray[i - 1]
    currentLine = wordRectanglePairArray[i]
    nextLine = wordRectanglePairArray[i + 1]

    # Check if there is a capital, lower pair in this line.
    # That means some sentence starts on the current line

    starti = -1
    startj = -1

    endi = -1
    endj = -1

    for j, wordRectanglePair in enumerate(currentLine):
        if len(wordRectanglePair.word) <= 1:
            continue

        if startj == -1 and wordRectanglePair.word[0].isupper() and wordRectanglePair.word[1].islower():
            starti = i
            startj = j
        elif wordRectanglePair.word[0].isupper() and wordRectanglePair.word[1].islower():
            endi = i
            endj = j

    if starti == -1:
        for j, wordRectanglePair in enumerate(prevLine):
            if len(wordRectanglePair.word) <= 1:
                continue

            if (
                wordRectanglePair.word[0].isupper()
                and wordRectanglePair.word[1].islower()
            ):
                starti = i - 1
                startj = j

    if endi == -1:
        for j, wordRectanglePair in enumerate(nextLine):
            if len(wordRectanglePair.word) <= 1:
                continue

            if (
                wordRectanglePair.word[0].isupper()
                and wordRectanglePair.word[1].islower()
            ):
                endi = i + 1
                endj = j - 1

    if starti == -1 or startj == -1:
        return ""

    sentence = ""
    curi = starti
    curj = startj

    while curi <= endi:
        sentence += wordRectanglePairArray[curi][curj].word + " "
        if curi == endi and curj == endj:
            break
        elif curj == len(wordRectanglePairArray[curi]) - 1:
            curi += 1
            curj = 0
        else:
            curj += 1


    return sentence
