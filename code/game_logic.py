import copy

class GameLogic:
    collected_territory_counts = {}
    def __init__(self):
        print("Game Logic Object Created")

    def score(self, prisoners, territory):
        return prisoners + territory

    def compute_controlled_terretories(self, boardArray):
        self.empty_squares = []
        self.collected_whites = []
        self.collected_blacks = []
        self.board_copy = copy.deepcopy(boardArray)
        self.queue = []
        self.collected_territory_counts = { 'white': 0, 'black': 0}
        self.boardWidth = len(boardArray)
        self.boardHeight = len(boardArray[0])

        while True:
            self.empty_squares = []
            self.collected_whites = []
            self.collected_blacks = []
            starting_point = self.find_empty_square(self.board_copy)

            if starting_point == None:
                break
            
            (startX, startY) = starting_point
            self.compute_controlled_territory(startX, startY)
            count = 0
            winner = 0
            if len(self.collected_whites) > 0 and len(self.collected_blacks) > 0:
                winner = 0
                count = 0
            elif len(self.collected_whites) > 0:
                winner = 1
                count = len(self.empty_squares)
                self.collected_territory_counts['white'] += count
            elif len(self.collected_blacks) > 0:
                winner = 2
                count = len(self.empty_squares)
                self.collected_territory_counts['black'] += count
            
            # removing visited squares from the board we are exploring
            for elm in self.collected_blacks:
                self.board_copy[elm[0]][elm[1]] = -1
            for elm in self.collected_whites:
                self.board_copy[elm[0]][elm[1]] = -1
            for elm in self.empty_squares:
                self.board_copy[elm[0]][elm[1]] = -1

        return self.collected_territory_counts

    def compute_controlled_territory(self, startX, startY):
        if self.board_copy[startX][startY] == 0 and not ((startX, startY) in self.empty_squares):
            self.empty_squares.append((startX,startY))
        elif self.board_copy[startX][startY] == 1 and not ((startX, startY) in self.collected_whites):
            self.collected_whites.append((startX,startY))
            return
        elif self.board_copy[startX][startY] == 2 and not ((startX, startY) in self.collected_blacks):
            self.collected_blacks.append((startX,startY))
            return 
        else:
            return
        
        if startX > 0:
            x = startX - 1
            y = startY       
            if (x,y) not in self.queue and (x,y) not in self.empty_squares and (x,y) not in self.collected_blacks and  (x,y) not in self.collected_whites:     
                self.queue.append((x,y))

        if startX < self.boardWidth - 1:
            x = startX + 1
            y = startY
            if (x,y) not in self.queue and (x,y) not in self.empty_squares and (x,y) not in self.collected_blacks and  (x,y) not in self.collected_whites:
                self.queue.append((x,y))

        if startY > 0:
            y = startY - 1
            x = startX
            if (x,y) not in self.queue and (x,y) not in self.empty_squares and (x,y) not in self.collected_blacks and  (x,y) not in self.collected_whites:
                self.queue.append((x,y))

        if startY < self.boardHeight - 1:
            y = startY + 1
            x = startX
            if (x,y) not in self.queue and (x,y) not in self.empty_squares and (x,y) not in self.collected_blacks and  (x,y) not in self.collected_whites:
                self.queue.append((x,y))

        while self.queue:
            item = self.queue.pop()
            self.compute_controlled_territory(item[0], item[1])

    def find_empty_square(self, board):
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == 0:
                    return (i, j)

        return None
