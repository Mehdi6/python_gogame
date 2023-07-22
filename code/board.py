from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF
from PyQt6.QtGui import QPainter, QColor, QBrush
from game_logic import GameLogic 

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(dict)  # signal sent when there is a new click location
    turnChangeSignal = pyqtSignal(int) #signal sent every time turn is chenged
    showWinnerSignal = pyqtSignal(tuple) #show the winner, sends the winner's infos to score board

    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 1000  # the timer updates every 1 millisecond
    counter = 30  # the number the counter will count down from
    maxGameDuration = 60
    frameWidth = 9
    frameHeight = 9
    painter = None
    gameLogic = None
    prisoners = {'white': 0, 'black': 0}  
    passesCount = [0, 0]

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        self.stopPice = True
        self.previousMove = [-1,-1,-1,-1] #index 0, 1 row, col => white; index 2,3 row, col => black

    def getScoreBoard(self):
        return self.scoreBoard

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer
        self.initBoardArray()
        self.gameLogic = GameLogic()
        self.printBoardArray()  # TODO - uncomment this method after creating the array above

    def initBoardArray(self):
        self.boardArray = [0] * 7  # TODO - create a 2d int/Piece array to store the state of the game
        for i in range(7):
            row = [0] * 7
            for j in range(7):
                row[j] = 0

            self.boardArray[i] = row

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        x, y = event.position().x(), event.position().y()

        x_pos = x - self.squareWidth()
        y_pos = y - self.squareHeight()

        if x_pos < 0 or y_pos < 0:
            return -1, -1

        col = int(round(x_pos / self.squareWidth()))
        row = int(round(y_pos / self.squareHeight()))

        return row, col

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / (self.frameWidth - 1)

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / (self.frameWidth - 1)

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")
        self.stopPice = False

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        if self.isStarted and event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                #!!! move to the next player
                print("press next")
                self.stopPice = True
            self.counter -= 1
            #print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''

        row, col = self.mousePosToColRow(event)
        #getting the current turn
        if row >= 0 and col >= 0 and self.stopPice == False:
            if self.suicideRule(row,col) == False and self.KOcheck(row,col) == False:# suicide check && KO check
                self.boardArray[row][col] = self.current_turn
                self.passesCount[self.current_turn - 1] = 0

                if self.current_turn == 1: #this move becomes the previos moove for white
                    self.previousMove[0] = row
                    self.previousMove[1] = col
                else:#this move becomes the previos moove for black
                    self.previousMove[2] = row
                    self.previousMove[3] = col
                self.update()
                # stoping the player form placeing moltiple pices:
                self.stopPice = True

                #go to the next player:
                self.nextTurn()

                self.captureBoardCheck()
            else:
                print("Suicide or KO not allowed")

        self.compute_territories()

    def compute_territories(self):
        collected_terretories = self.gameLogic.compute_controlled_terretories(self.boardArray)

        infosToPass = { 
            "white" : {"prisoners": self.prisoners['white'], "territories": collected_terretories["white"]}, 
            "black": {"prisoners":self.prisoners['black'] , "territories": collected_terretories["black"]}
            }

        self.clickLocationSignal.emit(infosToPass)

        return infosToPass

    def captureCheck(self,row,col):
        if self.boardArray[row][col] == 1:opposite = 2
        else: opposite = 1

        adversaries = 0
        supplyLines = 4
        if row-1 < 0 or row+1 >= 7 or col-1<0 or col+1 >= 7:
            supplyLines = 3
        if (row - 1 < 0 and col - 1 < 0) or (row - 1 < 0 and col + 1 >= 7) or (row + 1 >= 7 and col - 1 < 0) or (row + 1 >= 7 and col + 1 >= 7):
            supplyLines = 2

        #check for adversaries:
        if col-1 >= 0:
            if self.boardArray[row][col-1] == opposite:
                adversaries = adversaries + 1

        if row-1 >= 0:
            if self.boardArray[row-1][col] == opposite:
                adversaries = adversaries + 1

        if col+1 < 7:
            if self.boardArray[row][col+1] == opposite:
                adversaries = adversaries + 1

        if row+1 < 7:
            if self.boardArray[row+1][col] == opposite:
                adversaries = adversaries + 1

        if adversaries == supplyLines:
            return True
        return False

    def captureBoardCheck(self):
        for i in range(7):
            for j in range(7):
                if self.boardArray[i][j] != 0:
                    if self.captureCheck(i,j):
                        print("capture")
                        self.boardArray[i][j] = 0 #pice captured

    def KOcheck(self,row,col):
        if self.previousMove[self.current_turn] == -1:
            return False

        if self.current_turn == 1:#check white
            if self.previousMove[0] == row and self.previousMove[1] == col:
                return True
        else:#check black
            if self.previousMove[2] == row and self.previousMove[3] == col:
                return True

        return False

    def suicideRule(self, row, col):
        total = 0
        neededT = 8
        if row-1<0 or col-1<0 or row+1 >= 7 or col+1>=7:
            neededT = 5
        if (row-1<0 and col-1<0) or (row-1<0 and col+1>=7) or (row+1>=7 and col-1<0) or (row+1>=7 and col+1>=7):
            neededT = 3

        opposite = 1
        if self.current_turn == 1:
            opposite = 2

          #check col-1:
        if col-1 >= 0:
            if row-1>=0:
                if self.boardArray[row-1][col-1]==opposite:
                    total = total + 1
                if self.boardArray[row-1][col] == opposite:
                    total = total + 1

            if self.boardArray[row][col-1] == opposite:
                total = total + 1

            if row+1<7:
                if self.boardArray[row+1][col-1] == opposite:
                    total = total + 1
                if self.boardArray[row+1][col] == opposite:
                    total = total + 1

        #checking for col+1
        if col+1 < 7:
            if row-1>=0:
                if self.boardArray[row-1][col+1] == opposite:
                    total = total + 1

            if self.boardArray[row][col+1] == opposite:
                total = total + 1

            if row+1<7:
                if self.boardArray[row+1][col+1] == opposite:
                    total = total + 1

        if total == neededT:#sucide not allowed
            return True

        return False

    def resetGame(self):
        '''clears pieces from the board'''
        self.initBoardArray()
        self.counter = self.maxGameDuration
        self.current_turn = 2
        self.turnChangeSignal.emit(self.current_turn)
        self.update()
        self.stopPice = False

    def stopGame(self):
        self.isStarted = False
        

    def nextTurn(self, isPass = False):
        self.stopPice = False
        self.counter = self.maxGameDuration
        if isPass == True:
            print ("a pass " + str(self.passesCount[self.current_turn-1]))
            self.passesCount[self.current_turn-1] = self.passesCount[self.current_turn-1] + 1

            infosToPass = self.compute_territories()

            if self.passesCount[self.current_turn - 1] >= 2:
                self.stopGame()
                blackScore = self.gameLogic.score(infosToPass["white"]['prisoners'], infosToPass["white"]['territories'])
                whiteScore = self.gameLogic.score(infosToPass["black"]['prisoners'], infosToPass["black"]['territories'])
                winner = ((blackScore if self.current_turn == 1 else whiteScore), 2 if self.current_turn == 1 else 1)

                self.showWinnerSignal.emit(winner)
                self.passesCount = [0,0]

        if self.current_turn == 1:
            self.current_turn = 2
        else:
            self.current_turn = 1

        self.turnChangeSignal.emit(self.current_turn)

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        painter.translate(self.squareWidth(), self.squareHeight())
        '''draw all the square on the board'''

        for row in range(0, Board.boardHeight - 1):
            for col in range(0, Board.boardWidth - 1):
                painter.save()
                colTransformation = self.squareWidth() * col 
                rowTransformation = self.squareHeight() * row 
                outlineSize = 2
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(0, 0, int(self.squareWidth()), int(self.squareHeight()),
                                 QColor(0, 0, 0))  # TODO provide the required arguments
                painter.fillRect(int(outlineSize / 2), int(outlineSize / 2), int(self.squareWidth() - outlineSize),
                                 int(self.squareHeight() - outlineSize), QColor(207, 133, 77))
                painter.restore()

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        radius = self.squareWidth() / 4
        painter.translate(- radius, - radius)
        colour = Qt.GlobalColor.transparent  # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                colTransformation = self.squareWidth() * col  
                rowTransformation = self.squareHeight() * row  
                painter.translate(colTransformation, rowTransformation)
                color = self.boardArray[row][col]  # 0/ nothing 1/ white 2/ black
                if color == 0:
                    painter.restore()
                    continue

                center = QPointF(radius, radius)
                brush = QBrush(QColor(255, 255, 255) if color == 1 else QColor(0, 0, 0), Qt.BrushStyle.SolidPattern)
                painter.setBrush(brush)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
