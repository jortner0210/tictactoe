'''
Board Class for TicTacToe Game
'''
class Board:

    def __init__(self):
        self.board = [
            { 0: 0 }, { 1: 1 }, { 2: 2 },
            { 3: 3 }, { 4: 4 }, { 5: 5 }, 
            { 6: 6 }, { 7: 7 }, { 8: 8 }
        ]

    def _inBounds(self, position: int):
        '''
        Checks that given position is in bounds of game
        '''
        if position >= 0 and position <= 8:
            return True
        else:
            return False

    def resetBoard(self):
        '''
        Reset board to original state
        '''
        self.board = [
            { 0: 0 }, { 1: 1 }, { 2: 2 },
            { 3: 3 }, { 4: 4 }, { 5: 5 }, 
            { 6: 6 }, { 7: 7 }, { 8: 8 }
        ]

    def displayBoard(self):
        '''
        Print current state of board to the terminal
        '''
        print()
        print(" {} | {} | {}".format(self.board[0][0], self.board[1][1], self.board[2][2]))
        print("------------")
        print(" {} | {} | {}".format(self.board[3][3], self.board[4][4], self.board[5][5]))
        print("------------")
        print(" {} | {} | {}".format(self.board[6][6], self.board[7][7], self.board[8][8]))
        print()

    def checkForWinner(self):
        '''
        Checks the tokens in each column row and diagonal
        '''
        # Check columns
        if self.board[0][0] == self.board[3][3] and self.board[3][3] == self.board[6][6]: return self.board[0][0]
        if self.board[1][1] == self.board[4][4] and self.board[4][4] == self.board[7][7]: return self.board[1][1]
        if self.board[2][2] == self.board[5][5] and self.board[5][5] == self.board[8][8]: return self.board[2][2]
        # Check rows
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]: return self.board[0][0]
        if self.board[3][3] == self.board[4][4] and self.board[4][4] == self.board[5][5]: return self.board[3][3]
        if self.board[6][6] == self.board[7][7] and self.board[7][7] == self.board[8][8]: return self.board[6][6]
        # Check diagonals
        if self.board[0][0] == self.board[4][4] and self.board[4][4] == self.board[8][8]: return self.board[0][0]
        if self.board[2][2] == self.board[4][4] and self.board[4][4] == self.board[6][6]: return self.board[2][2]

        return None

    def atPosition(self, position: int):
        '''
        Returns token at position
        Must be between 0 and 8
        '''
        if self._inBounds(position):
            return self.board[position][position]
        else: return None

    def positionAvailable(self, position: int):
        '''
        Checks whether a position is available
        lambda checks that a position is equal to the value on board
        if not true then the position is not available
        '''
        for i in range(8):
            if not (lambda x : x == self.board[x][x])(i): return False
        return True


    def placeToken(self, position: int, token: str):
        '''
        Places a token on the board if position is in correct range
        '''
        if self._inBounds(position):
            self.board[position][position] = token
            return True
        else: return False


'''
Player Class for TicTacToe Game
'''
class Player:

    def __init__(self, token: str):
        self.checkTokenType(token)
        self.token = token

    def placeToken(self, board: Board, position: int):
        '''
        Places a token on the board using player token
        '''
        return board.placeToken(position, self.token)

    def checkTokenType(self, token: str):
        '''
        Raises error if token is not a string
        Important to require string to avoid bugs when placing token on board
        '''
        if type(token) != str: raise ValueError("Player token must be of type string")


class TicTacToe:

    def __init__(self):
        self.board = Board()






def main():
    '''
    For debugging
    '''
    board = Board()
    player = Player('x')
    board.displayBoard()
    board.positionAvailable(0)
    player.placeToken(board, 0)
    board.displayBoard()
    board.positionAvailable(0)


if __name__ == '__main__':
    main()