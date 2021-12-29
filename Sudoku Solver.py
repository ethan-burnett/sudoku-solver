# Sudoku Solver
# Solves sudoku via a recursive method
# Ethan Burnett   27 December 2021

SIZE = 9

class Square():
    def __init__(self, rGrid, value=0, impNums=set(), id=0) -> None:
        self.aValue : int   = value
        self.id : int       = id
        self.rRow : Row     = None
        self.rCol : Col     = None
        self.rBox : Box     = None
        self.rGrid : Grid   = rGrid
        self.impossibleNumbers = impNums.copy()
    
    def setValue(self, value : int):
        if self.aValue != 0:
            print("Invalid value: " + str(value) + " for id: " + str(self.id))
            quit()
        self.aValue = value
    
    def flagImpossibleNumber(self, number : int) -> None:
        self.impossibleNumbers.add(number)
    
    def __repr__(self) -> str:
        if self.aValue == 0:
            return " "
        return str(self.aValue)
    
    def possibleNumbers(self) -> list:
        nums = []
        for num in range(1, 10):
            if num in self.impossibleNumbers or self.rRow.containsNum(num) or self.rCol.containsNum(num) or self.rBox.containsNum(num):
                continue
            nums.append(num)
        return nums
    
    def isValid(self) -> bool:
        value, result = self.aValue, True
        self.aValue = 0
        if self.rRow.containsNum(value) or self.rCol.containsNum(value) or self.rBox.containsNum(value):
            result = False
        self.aValue = value
        return result

class Row():
    def __init__(self, rGrid, rowNum) -> None:
        self.rGrid : Grid   = rGrid
        self.allSquares     = self.rGrid.allSquares[rowNum*SIZE : (rowNum+1)*SIZE]
        for square in self.allSquares:
            square.rRow = self
    
    def __repr__(self) -> str:
        row = "||"
        for i, square in enumerate(self.allSquares):
            row += " " + str(square) + " "
            if i % 3 == 2:
                row += "||"
            else:
                row += "|"
        return row
    
    def containsNum(self, num: int) -> bool:
        for square in self.allSquares:
            if square.aValue == num:
                return True
        return False

class Col():
    def __init__(self, rGrid, colNum) -> None:
        self.rGrid : Grid   = rGrid
        self.allSquares = []
        for row in self.rGrid.allRows:
            self.allSquares.append(row.allSquares[colNum])
            row.allSquares[colNum].rCol = self
    
    def containsNum(self, num: int) -> bool:
        for square in self.allSquares:
            if square.aValue == num:
                return True
        return False

class Box():
    def __init__(self, rGrid, boxNum) -> None:
        self.rGrid : Grid   = rGrid
        if boxNum in [0, 1, 2]:
            rows = self.rGrid.allRows[0:3]
        elif boxNum in [3, 4, 5]:
            rows = self.rGrid.allRows[3:6]
        elif boxNum in [6, 7, 8]:
            rows = self.rGrid.allRows[6:9]
        lowIndex    = (boxNum % 3) * 3
        highIndex   = ((boxNum % 3) + 1) * 3
        self.allSquares = []
        for row in rows:
            self.allSquares = self.allSquares + row.allSquares[lowIndex:highIndex]
        for square in self.allSquares:
            square.rBox = self
    
    def containsNum(self, num: int) -> bool:
        for square in self.allSquares:
            if square.aValue == num:
                return True
        return False

class Grid():
    def __init__(self, values) -> None:
        if not type(values[0]) is tuple:
            self.allSquares = [Square(self, value, id=i) for i, value in enumerate(values)]
        else:
            i, self.allSquares = 0, []
            for value, impNums in values:
                self.allSquares.append(Square(rGrid=self, value=value, impNums=impNums, id=i))
                i = i + 1
        self.allRows    = [Row(rGrid=self, rowNum=i) for i in range(SIZE)]
        self.allCols    = [Col(rGrid=self, colNum=i) for i in range(SIZE)]
        self.allBoxes   = [Box(rGrid=self, boxNum=i) for i in range(SIZE)]
    
    def getSquares(self) -> list:
        return [(square.aValue, square.impossibleNumbers) for square in self.allSquares]
    
    def __repr__(self) -> str:
        big = "||===|===|===||===|===|===||===|===|===||"
        lit = "||---|---|---||---|---|---||---|---|---||"
        grid = "||===========||===========||===========||\n"
        for i, row in enumerate(self.allRows):
            grid += str(row) + "\n"
            if i == SIZE - 1:
                break
            if i % 3 == 2:
                grid += big + "\n"
            else:
                grid += lit + "\n"
        grid += "||===========||===========||===========||\n"
        return grid
    
    def copy(self):
        return Grid(values=self.getSquares())
    
    def nextSquare(self):
        bestSquare = None
        bestPosNumbers = [i for i in range(10)]
        for square in self.allSquares:
            if square.aValue != 0: continue
            posNumbers = square.possibleNumbers()
            if len(posNumbers) < len(bestPosNumbers):
                bestSquare = square
                bestPosNumbers = posNumbers
            if len(bestPosNumbers) == 0: break
        return (bestPosNumbers, bestSquare)
    
    def solve(self, depth=5):
        while True:
            possibleNumbers, square = self.nextSquare()
            if square is None:
                return self
            if len(possibleNumbers) == 0:
                # print("No possible numbers")
                return None
            if len(possibleNumbers) == 1:
                square.setValue(possibleNumbers[0])
            elif depth <= 0:
                print("*" * 20 + "\nDepth Reached\n" + "*" * 20)
                return self
            else:
                # print("Copying")
                copyGrid = self.copy()
                copyGrid.allSquares[square.id].setValue(possibleNumbers[0])
                result = copyGrid.solve(depth=depth-1)
                if not result is None:
                    return result
                # del(copyGrid)
                square.flagImpossibleNumber(possibleNumbers[0])
    
    def isSolved(self) -> bool:
        for square in self.allSquares:
            if not square.isValid():
                return False
        return True




values_2 = [
    5, 3, 0,    0, 7, 0,    0, 0, 0,
    6, 0, 0,    1, 9, 5,    0, 0, 0,
    0, 9, 8,    0, 0, 0,    0, 6, 0,

    8, 0, 0,    0, 6, 0,    0, 0, 3,
    4, 0, 0,    8, 0, 3,    0, 0, 1,
    7, 0, 0,    0, 2, 0,    0, 0, 6,

    0, 6, 0,    0, 0, 0,    2, 8, 0,
    0, 0, 0,    4, 1, 9,    0, 0, 5,
    0, 0, 0,    0, 8, 0,    0, 7, 9
]

values_1 = [
    8, 0, 0,    0, 0, 0,    0, 0, 0,
    0, 0, 3,    6, 0, 0,    0, 0, 0,
    0, 7, 0,    0, 9, 0,    2, 0, 0,

    0, 5, 0,    0, 0, 7,    0, 0, 0,
    0, 0, 0,    0, 4, 5,    7, 0, 0,
    0, 0, 0,    1, 0, 0,    0, 3, 0,

    0, 0, 1,    0, 0, 0,    0, 6, 8,
    0, 0, 8,    5, 0, 0,    0, 1, 0,
    0, 9, 0,    0, 0, 0,    4, 0, 0
]

print("\n\nExample Sudoku\n")

grid = Grid(values=values_1)
grid = grid.solve(20)
if not grid is None and grid.isSolved():
    print(grid)
else:
    print("*" * 20 + "\nNot Solved\n" + "*" * 20)
    print(grid)

print("\n\nHarder Example Sudoku\n")

grid = Grid(values=values_1)
grid = grid.solve(20)
if not grid is None and grid.isSolved():
    print(grid)
else:
    print("*" * 20 + "\nNot Solved\n" + "*" * 20)
    print(grid)
