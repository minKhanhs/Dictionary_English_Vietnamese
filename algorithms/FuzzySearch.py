from config.app_config import AppConfig
from structures.trie import TrieNode
from algorithms.Levenshtein import Levenshtein

# Tìm kiếm gần đúng (fuzzy search) trong Trie bằng thuật toán Levenshtein.
class FuzzySearch:
    def __init__(self, trieRoot: TrieNode):
        self.trieRoot = trieRoot
        self.allWords = []
        self.extractAllWords(trieRoot)
    
    def extractAllWords(self, node: TrieNode, currentWord: str = ""):
        if node.isEndOfWord:
            self.allWords.append(currentWord)
        
        for char, childNode in node.children.items():
            self.extractAllWords(childNode, currentWord + char)

    def getMaxDistance(self, wordLength: int) -> int:
        if wordLength <= AppConfig.SHORT_WORD_LENGTH:
            return AppConfig.SHORT_WORD_DISTANCE
        elif wordLength <= AppConfig.MEDIUM_WORD_LENGTH:
            return AppConfig.MEDIUM_WORD_DISTANCE
        else:
            return AppConfig.LONG_WORD_DISTANCE

    def searchRecursive(self, node: TrieNode, letter: str, currentWord: str, 
                          previousRow: list, levCalculator: Levenshtein, 
                          maxCost: int, results: list):
        """Tìm kiếm đệ quy trong cây Trie"""
        
        currentRow = levCalculator.calculateNextRow(previousRow, letter)

        if currentRow[-1] <= maxCost and node.isEndOfWord:
            results.append((currentWord, currentRow[-1]))

        if min(currentRow) <= maxCost:
            for nextLetter, nextNode in node.children.items():
                self.searchRecursive(
                    nextNode, 
                    nextLetter, 
                    currentWord + nextLetter, 
                    currentRow, 
                    levCalculator,
                    maxCost, 
                    results
                )

    def getSuggestions(self, targetWord: str) -> list:
        """Lấy danh sách gợi ý từ"""
        if not targetWord or len(targetWord) > AppConfig.MAX_WORD_LENGTH:
            return []

        targetWordLower = targetWord.lower()
        maxCost = self.getMaxDistance(len(targetWordLower))
        results = []
        
        levCalculator = Levenshtein(targetWordLower)
        initialRow = levCalculator.getInitialRow()

        for letter, node in self.trieRoot.children.items():
            self.searchRecursive(
                node, 
                letter, 
                letter, 
                initialRow, 
                levCalculator, 
                maxCost, 
                results
            )

        results.sort(key=lambda x: (x[1], x[0]))
        suggestions = [res[0] for res in results[:AppConfig.MAX_SUGGESTIONS]]
        
        return suggestions
