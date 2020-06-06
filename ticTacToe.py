'''
Board Class for TicTacToe Game
'''
class Board:

    def __init__(self):
        self.board = [
            { 0: 0 }, { 1: 1 }, { 2: 2 },
            { 3: 0 }, { 4: 4 }, { 5: 5 }, 
            { 6: 0 }, { 7: 7 }, { 8: 8 }
        ]

    def _inBounds(self, position: int):
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
        print(' {} | {} | {}'.format(self.board[0][0], self.board[1][1], self.board[2][2]))
        print('------------')
        print(' {} | {} | {}'.format(self.board[3][3], self.board[4][4], self.board[5][5]))
        print('------------')
        print(' {} | {} | {}'.format(self.board[6][6], self.board[7][7], self.board[8][8]))
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

    def __init__(self, token):
        self.token = token

    def placeToken(self, board: Board, position: int):
        '''
        Places a token on the board using player token
        '''
        return board.placeToken(position, self.token)


class TicTacToe:

    def __init__(self):
        self.board = Board()









def main():
    board = Board()
    board.displayBoard()
    print(board.checkForWinner())


if __name__ == '__main__':
    main()