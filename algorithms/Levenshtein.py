class Levenshtein:
    def __init__(self, targetWord: str):
        self.targetWord = targetWord.lower()
        self.targetLength = len(targetWord)

    def getInitialRow(self) -> list:
        return list(range(self.targetLength + 1))

    def calculateNextRow(self, previousRow: list, currentLetter: str) -> list:
        columns = self.targetLength + 1
        currentRow = [previousRow[0] + 1]

        for column in range(1, columns):
            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1

            # Chi phí thay thế (0 nếu giống nhau, 1 nếu khác nhau)
            if self.targetWord[column - 1] != currentLetter:
                replaceCost = previousRow[column - 1] + 1
            else:
                replaceCost = previousRow[column - 1]

            currentRow.append(min(insertCost, deleteCost, replaceCost))

        return currentRow

    def distance(self, inputWord: str) -> int:
        """Tính Levenshtein Distance"""
        inputWord = inputWord.lower()

        if not inputWord:
            return self.targetLength
        if not self.targetWord:
            return len(inputWord)

        previousRow = self.getInitialRow()

        for char in inputWord:
            previousRow = self.calculateNextRow(previousRow, char)

        return previousRow[-1]
