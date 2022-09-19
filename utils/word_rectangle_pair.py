class WordRectanglePair:
    def __init__(self, word, rect, translated):
        self.word = word
        self.rect = rect
        self.translated = translated
    def __str__(self):
        return "Current word: "+self.word+" at: ["+str(self.rect.minX)+","+str(self.rect.minY)+"]"+" translated word: "+self.translated
    
