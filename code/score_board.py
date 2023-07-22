import sys
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QFrame
from PyQt6.QtCore import pyqtSlot


class Separator(QFrame):
    def __init__(self):
        super(Separator, self).__init__()
        self.setObjectName("line")
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''
    game_started = False
    myPopup = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.help_button = QPushButton("Rules of the game")

        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.label_score = QLabel("Score: ")
        self.label_turn = QLabel("Turn: ")
        self.blackPlayerLabel = QLabel("Black Player")
        self.whitePlayerLabel = QLabel("White Player")

        self.whitePrisonersNumber = QLabel("Number of prisoners: ")
        self.blackPrisonersNumber = QLabel("Number of prisoners: ")
        self.blackTerritoryControlled = QLabel("Territory Controlled: ")
        self.whiteTerritoryControlled = QLabel("Territory Controlled: ")

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(
            "background-color: green; color: white;font-family: \"Courier New\", Courier, sans-serif;")

        self.help_button.setStyleSheet(
            "background-color: gray; color: white;font-family: \"Courier New\", Courier, sans-serif;")

        self.help_button.clicked.connect(self.show_how_to_play)
        self.mainLayout.addWidget(self.help_button)
        self.start_button.clicked.connect(self.start_game)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_score)
        self.mainLayout.addWidget(self.label_turn)

        # we add first separator
        self.mainLayout.addWidget(Separator())
        self.mainLayout.addWidget(self.blackPlayerLabel)
        self.mainLayout.addWidget(self.blackPrisonersNumber)
        self.mainLayout.addWidget(self.blackTerritoryControlled)

        # we add second separator
        self.mainLayout.addWidget(Separator())
        self.mainLayout.addWidget(self.whitePlayerLabel)
        self.mainLayout.addWidget(self.whitePrisonersNumber)
        self.mainLayout.addWidget(self.whiteTerritoryControlled)

        # we add third separator
        self.mainLayout.addWidget(Separator())

        self.mainLayout.addWidget(self.start_button)
        self.loadGameInstructions()
        self.setWidget(self.mainWidget)
        self.show()

    def initWidgets(self):
        self.label_timeRemaining.setText("Time remaining: ")
        self.label_score.setText("Score: ")
        self.label_score.setStyleSheet(
            "background-color: gray; color: white;font-family: \"Courier New\", Courier, sans-serif;")
        self.label_turn.setText("Turn: ")
        self.blackPlayerLabel.setStyleSheet(
            "background-color: gray; color: white;font-family: \"Courier New\", Courier, sans-serif;")
        self.blackPlayerLabel.setText("Black Player")
        self.whitePlayerLabel.setStyleSheet(
            "background-color: gray; color: white;font-family: \"Courier New\", Courier, sans-serif;")
        self.whitePlayerLabel.setText("White Player")

        self.whitePrisonersNumber.setText("Number of prisoners: ")
        self.blackPrisonersNumber.setText("Number of prisoners: ")
        self.blackTerritoryControlled.setText("Territory Controlled: ")
        self.whiteTerritoryControlled.setText("Territory Controlled: ")

    def loadGameInstructions(self):
        self.gameInstructions = " Explanation of the Game:\n" \
                                "Go \"encircling game\" is an abstract strategy board game for two players,\n" \
                                " in which the aim is to surround more territory than the opponent. \n" \
                                "The game was invented in China over 3,000 years ago, and is therefore\n" \
                                " believed to be the oldest board game continuously played today. It was\n" \
                                " considered one of the four essential arts of the cultured aristocratic \n" \
                                "Chinese scholars in antiquity. Despite its relatively simple rules, Go is \n" \
                                "very complex, even more so than chess. \n" \
                                "\n" \
                                "Movements:\n" \
                                "Black plays first, with black and white taking turns. A stone can be placed\n" \
                                " at any unoccupied intersection of the board with limited exceptions. \n" \
                                "1. Suicide Rule:\n " \
                                "You cannot place a stone which will immediately have no liberties. \n" \
                                "2. KO Rule (Eternity Rule): \n" \
                                "Previous game states are not allowed.\n"

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        #connect each time the turn is chenged from board
        board.turnChangeSignal.connect(self.setTurn)
        #connect each time the turn is chenged from board
        board.showWinnerSignal.connect(self.showWinner)

        self.board = board

    @pyqtSlot(dict)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, scoreInfos):
        self.whitePrisonersNumber.setText("Number of prisoners: " + str(scoreInfos["white"]["prisoners"]))
        self.blackPrisonersNumber.setText("Number of prisoners: " + str(scoreInfos["black"]["prisoners"]))
        self.whiteTerritoryControlled.setText("Territory Controlled: " + str(scoreInfos["white"]["territories"]))
        self.blackTerritoryControlled.setText("Territory Controlled: " + str(scoreInfos["black"]["territories"]))
    
    def setTurn(self, turn):
        if turn == 1:
            update = "Turn: White"
        else:
            update = "Turn: Black"

        self.label_turn.setText(update)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        # self.redraw()

    def start_game(self):
        if self.game_started == True:
            # we can just reset the game in this case
            self.board.resetGame()
            self.initWidgets()
        else:
            # the game has started for the first time
            self.board.start()
            self.start_button.setText("Reset")
            self.start_button.clicked.connect(self.start_game)
            # we add the pass button for the player to pass the turn
            self.pass_button = QPushButton("Pass")
            self.pass_button.setStyleSheet(
                "background-color: blue; color: white;font-family: \"Courier New\", Courier, sans-serif;")
            self.pass_button.clicked.connect(self.pass_game)
            self.mainLayout.addWidget(self.pass_button)
            self.game_started = True
            self.setTurn(self.board.current_turn)

    @pyqtSlot(tuple) 
    def showWinner(self, winner):
        print (winner)
        if winner[1] == 1:
            self.whitePlayerLabel.setText("White Player WINNER")
            self.whitePlayerLabel.setStyleSheet(
                "background-color: green; color: white;font-family: \"Courier New\", Courier, sans-serif;")
        else:
            self.blackPlayerLabel.setText("Black Player WINNER")
            self.blackPlayerLabel.setStyleSheet(
                "background-color: green; color: white;font-family: \"Courier New\", Courier, sans-serif;")

        self.label_score.setText("Winner Score: " + str(winner[0]))
        self.label_score.setStyleSheet(
                "background-color: red; color: white;font-family: \"Courier New\", Courier, sans-serif;")
    
    def pass_game(self):
        self.board.nextTurn(True)
        self.setTurn(self.board.current_turn)

    def show_how_to_play(self):
        self.myPopup = QWidget()
        self.myPopup.resize(300, 150)
        self.myPopup.setWindowTitle("Rules of Go.")
        myPopLayout = QVBoxLayout()
        self.myPopup.setLayout(myPopLayout)
        myTextLabel = QLabel(self.gameInstructions)
        myPopLayout.addWidget(myTextLabel)
        self.myPopup.show()