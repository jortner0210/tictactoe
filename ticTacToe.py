import random


'''
Board Class for TicTacToe Game
'''
class TTTBoard:

    def __init__(self):
        self._board = [
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ]

    def _inBounds(self, position: int):
        '''
        Checks that given position is in bounds of game
        '''
        if position >= 0 and position <= 8:
            return True
        else:
            return False

    def boardState(self):
        '''
        Returns copy of the current board state
        '''
        return self._board.copy()

    def reset(self):
        '''
        Reset board to original state
        '''
        self._board = [
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ]

    def display(self):
        '''
        Print current state of board to the terminal
        '''
        print()
        print(" {} | {} | {}".format(self._board[0], self._board[1], self._board[2]))
        print("------------")
        print(" {} | {} | {}".format(self._board[3], self._board[4], self._board[5]))
        print("------------")
        print(" {} | {} | {}".format(self._board[6], self._board[7], self._board[8]))
        print()

    def checkForWinner(self):
        '''
        Checks the tokens in each column row and diagonal
        '''
        # Check columns
        if self._board[0] == self._board[3] and self._board[3] == self._board[6]: return self._board[0]
        if self._board[1] == self._board[4] and self._board[4] == self._board[7]: return self._board[1]
        if self._board[2] == self._board[5] and self._board[5] == self._board[8]: return self._board[2]
        # Check rows
        if self._board[0] == self._board[1] and self._board[1] == self._board[2]: return self._board[0]
        if self._board[3] == self._board[4] and self._board[4] == self._board[5]: return self._board[3]
        if self._board[6] == self._board[7] and self._board[7] == self._board[8]: return self._board[6]
        # Check diagonals
        if self._board[0] == self._board[4] and self._board[4] == self._board[8]: return self._board[0]
        if self._board[2] == self._board[4] and self._board[4] == self._board[6]: return self._board[2]

        return None

    def isFull(self):
        '''
        Check if the board is full
        '''
        for i in range(8):
            if self.positionAvailable(i): return False
        return True

    def atPosition(self, position: int):
        '''
        Returns token at position
        Must be between 0 and 8
        '''
        if self._inBounds(position):
            return self._board[position][position]
        else: return None

    def positionAvailable(self, position: int):
        '''
        Checks whether a position is available
        if a positions board value is equal to the position index
        then the position is available
        '''
        if not (lambda x : x == self._board[x])(position): return False
        return True

    def placeToken(self, position: int, token: str):
        '''
        Places a token on the board if position is in correct range
        and the position is available
        '''
        if self.isValidMove(position):
            self._board[position] = token
            return True
        else: return False

    def isValidMove(self, position: int):
        '''
        Ensures the position is available and the position is within
        the bounds of the game board
        '''
        if self._inBounds(position) and self.positionAvailable(position): return True
        else: return False


'''
Player Class for TicTacToe Game
For use by human player
'''
class TTTPlayer:

    def __init__(self, token: str):
        self._checkTokenType(token)
        self._token = token

    def _checkTokenType(self, token: str):
        '''
        Raises error if token is not a string
        Important to require string to avoid bugs when placing token on board
        '''
        if type(token) != str: raise ValueError("Player token must be of type string")

    def placeToken(self, board: TTTBoard, position: int):
        '''
        Places a token on the board using player token
        '''
        return board.placeToken(position, self._token)

    def getToken(self):
        '''
        Return player token
        '''
        return self._token

    def getMove(self, board: TTTBoard):
        '''
        Return player move when a valid input is given
        '''
        while True:
            player_input = input("Player {}. Enter move: ".format(self._token))
            if player_input.isnumeric():
                player_input = int(player_input)
                if board.isValidMove(player_input):
                    return player_input


'''
Agent Class for TicTacToe Game
For use by automated player
'''
class TTTAgent(TTTPlayer):

    def getMove(self, board: TTTBoard):
        return self.getRandomMove(board)

    def getRandomMove(self, board: TTTBoard):
        '''
        Returns randomly chosen move
        '''
        while True:
            move = random.randint(0, 8)
            if board.isValidMove(move): 
                print("Player {}. Move : {}".format(self._token, move))
                return move


'''
Class to run a game between two players
'''
class TicTacToe:

    def __init__(self, p_1: TTTPlayer, p_2: TTTPlayer, display: bool = False):
        '''
        _results : all actions and board states of each game
        '''
        self._board   = TTTBoard()
        self._players = [p_1, p_2]
        self._results = []
        self._display = display

    def _getNextPlayer(self, current_player: int):
        '''
        Returns the next player
        '''
        if current_player == 1: return 0
        else: return 1

    def shufflePlayers(self):
        '''
        Shuffle the order of the players
        '''
        random.shuffle(self._players)
    
    def playGame(self):
        '''
        Play through game
        Current play is denoted by 0 or 1 - position is _players array
        Players are shuffled before the start of each game
        '''
        self._board.reset()
        self.shufflePlayers()
        game_over   = False
        curr_player = 0
        if self._display: self._board.display()
        game_data = {
            'board_states': [],
            'winner'      : ''
        }
        # game loop
        while not game_over:
            # add current board state
            game_data['board_states'].append(self._board.boardState())
            player_input = self._players[curr_player].getMove(self._board)
            self._players[curr_player].placeToken(self._board, player_input)
            # check for winner
            winner = self._board.checkForWinner()
            if winner is not None:
                # game over : winner
                game_data['winner'] = winner
                if self._display: print("Game Over: Winner player token {}".format(winner))
                break
            # check for draw
            if self._board.isFull():
                # game over : draw
                game_data['winner'] = 'draw'
                if self._display: print("Game Over : Draw")
                break
            # switch player
            curr_player = self._getNextPlayer(curr_player)
            if self._display: self._board.display()
        # append final board state
        game_data['board_states'].append(self._board.boardState())
        # append game data to results memeber
        self._results.append(game_data)
        if self._display: self._board.display()
    

def main():
    '''
    For debugging
    '''
    player_1 = TTTAgent('X')
    player_2 = TTTAgent('O')
    ttt_game = TicTacToe(player_1, player_2, True)
    ttt_game.playGame()


if __name__ == '__main__':
    main()