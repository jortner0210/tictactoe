from ticTacToe import TTTPlayer
from ticTacToe import TTTBoard
from ticTacToe import TicTacToe
import random

'''
Agent Class for TicTacToe Game
For use by automated player
'''
class TTTAgent(TTTPlayer):
    '''
    - https://medium.com/@carsten.friedrich/part-3-tabular-q-learning-a-tic-tac-toe-player-that-gets-better-and-better-fa4da4b0892a
    1) create q table with a row for every possible state
    and initialize values to be the same - 1 : optimistic, 0: pessimistic
    2) play tictactoe and at the end of each game, update 
    q values of all move in game according to final game result
    2a) last move -> win = 1, loss = 0, draw = 0.5
    2b) every other move -> Q(S,A) = Q(S,A)+α∗(γ∗maxaQ(S′,a)− Q(S,A))
                         -> Q(S,A)=(1−α)∗Q(S,A)+α∗γ∗maxaQ(S′,a)
        - S′ : next state
        - α  : learning rate - default = 0.9
        - γ  : discount factor - default = 0.95
        - maxaQ(S′,a) : q value of best move in following state
    '''

    def getMove(self, board: TTTBoard):
        # Policy :
        # get hash value of current borad state
        # get possible moves from board state
        # choose move with highest value
        # if multiple moves have the same value, pick randomly
        return self.getRandomMove(board)

    def getRandomMove(self, board: TTTBoard):
        '''
        Returns randomly chosen move
        '''
        while True:
            move = random.randint(0, 8)
            if board.isValidMove(move): 
                #print("Player {}. Move at position : {}".format(self._token, move))
                return move


'''
Always chooses random move
'''
class TTTRandomAgent(TTTPlayer):

    def getMove(self, board: TTTBoard):
        return self.getRandomMove(board)

    def getRandomMove(self, board: TTTBoard):
        '''
        Returns randomly chosen move
        '''
        while True:
            move = random.randint(0, 8)
            if board.isValidMove(move): 
                return move



def main():
    '''
    For debugging
    '''
    player_1 = TTTRandomAgent('X')
    player_2 = TTTRandomAgent('O')
    ttt_game = TicTacToe(player_1, player_2, True)
    for i in range(10):
        ttt_game.playGame()
        input("Play next game")
    ttt_game.displayWinners()
    ttt_game.displayResults()

if __name__ == '__main__':
    main()