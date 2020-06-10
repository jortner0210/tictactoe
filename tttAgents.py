from ticTacToe import TTTPlayer
from ticTacToe import TTTBoard
from ticTacToe import TicTacToe
import time
import pprint
import random
import operator
import math


'''
TTT Agent that always chooses a random move
'''
class TTTRandomAgent(TTTPlayer):

    def passReward(self, reward: float, state_actions: list):
        pass

    def getMove(self, board: TTTBoard):
        return self.getRandomMove(board)


'''
Agent Class for TicTacToe Game
For use by automated player
'''
class TTTQAgent(TTTPlayer):
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
    def __init__(self, token: str):
        TTTPlayer.__init__(self, token)
        self._train       = False
        self._epsilon     = 1.0
        self._epsi_decay  = 0.9993
        self._epsi_min    = 0.005
        self._alpha       = 0.2
        self._discount    = 0.95
        self._init_q_val  = 0.5
        self._q_table     = { 
            # "hash": { pos_val: q_val }, ...
        }

    def _getMaxQMove(self, board: TTTBoard):
        '''
        Return move with the highest q value for given board state
        If board state not in table, add it, initialize values and 
        return random move
        '''
        # check if others have same value, choose randomly
        board_hash = board.getHash()
        try:
            moves     = self._q_table[board_hash]
            max_value = max(moves.items(), key=operator.itemgetter(1))[0]
            return max_value 
        except:
            self._addHash(board_hash, board.validMovesForHash(board_hash))
            return self.getRandomMove(board)

    def _getMaxQFromHash(self, state_hash: str):
        try:
            moves = self._q_table[state_hash]
            return max([moves[key] for key in moves.keys()])
        except:
            return self._init_q_val

    def _addHash(self, board_hash: str, available_moves: list):
        '''
        Add hash to state table
        '''
        state_action_values = { }
        for move in available_moves:
            state_action_values[move] = random.uniform(0, 1)
        self._q_table[board_hash] = state_action_values

    def _addReward(self, reward: float, action: int, state_hash: str):
        '''
        Add reward to state action's q value
        '''
        try:
            self._q_table[state_hash][action] += reward
        except:
            self._addHash(state_hash, TTTBoard.validMovesForHash(state_hash))
            self._q_table[state_hash][action] += reward

    def _setQValue(self, new_value: float, action: int, state_hash: str):
        '''
        Set state action's q value to new value
        '''
        try:
            self._q_table[state_hash][action] = new_value
        except:
            self._addHash(state_hash, TTTBoard.validMovesForHash(state_hash))
            self._q_table[state_hash][action] = new_value

    def _getQValue(self, state_hash: str, action: int):
        '''
        Returns the q-value of given state and action
        '''
        try:
            return self._q_table[state_hash][action]
        except:
            self._addHash(state_hash, TTTBoard.validMovesForHash(state_hash))
            return self._init_q_val


    def _calcReward(self, state_hash: str, action: int, max_next_q: float):
        '''
        Calculates : α∗(γ∗maxaQ(S′,a)− Q(S,A))
        - max_next_q = maxaQ(S′,a)
        '''
        return self._alpha * (self._discount * max_next_q - self._getQValue(state_hash, action))

    def _calcNewQValue(self, state_hash: str, action: int, reward: int, max_next_q: float):
        '''
        '''
        return ((1 - self._alpha) * self._getQValue(state_hash, action)) + self._alpha * (reward + (self._discount * max_next_q))

    def setEpsilonDecay(self, decay: float):
        '''
        Set epsilon decay value
        '''
        self._epsi_decay = decay

    def getQTable(self):
        '''
        Returns a copy of the q table
        '''
        return self._q_table.copy()

    def getEpsilon(self):
        '''
        Return epsilon value
        '''
        return self._epsilon

    def trainAgent(self, train: bool):
        '''
        Set memeber that denotes whether the model should be training or not
        '''
        self._train = train

    def passReward(self, reward: float, state_actions: list):
        '''
        state_actions : list of state hashes and move made on state as a tuple
        i.e. (hash, action)
        last state_action is the terminal state and shouldn't be updated
        '''
        if self._train:
            #print("token {} - reward {}".format(self._token, reward))
            #pprint.pprint(state_actions)
            #input()
            prev_hash   = state_actions[-1][0]
            prev_action = state_actions[-1][1] 
            #print(state_actions[-2][0])
            #print(state_actions[-2][1])
            #print(state_actions[-1][0])
            #print(state_actions[-1][1])
            #input()

            #new_q = self._calcNewQValue(prev_hash, prev_action, reward, self._getMaxQFromHash(state_actions[-1][0]))
            self._addReward(reward, prev_action, prev_hash)
            new_q = self._getMaxQFromHash(prev_hash)
            self._setQValue(new_q, prev_action, prev_hash)
            reward = new_q
            max_next_q = self._getMaxQFromHash(prev_hash)

            i = len(state_actions) - 2 
            # Reverse list from second to last element to beginning
            while i >= 0:
                curr_hash   = state_actions[i][0]
                curr_action = state_actions[i][1]
                #print(state_actions[i][0])
                #print(state_actions[i][1])
                #input()
                
                new_q = self._calcNewQValue(curr_hash, curr_action, reward, max_next_q)
                self._setQValue(new_q, curr_action, curr_hash)
                reward = new_q
                prev_hash   = curr_hash
                prev_action = curr_action
                max_next_q  = self._getMaxQFromHash(prev_hash)
                
                i -= 1

            # Decay exploration rate
            if self._epsilon >= self._epsi_min:
                self._epsilon *= self._epsi_decay
            return

    

    def getMove(self, board: TTTBoard):
        '''
        Policy : get hash value of current borad state
                 get possible moves from board state
                 choose move with highest value
                 if multiple moves have the same value, pick randomly
        '''
        if random.uniform(0, 1) > self._epsilon: return self._getMaxQMove(board)
        else: return self.getRandomMove(board)



class TTTMiniMaxAgent(TTTPlayer):

    def __init__(self, token: str):
        TTTPlayer.__init__(self, token)
        self._rewards = {
            self._token: 1,
            "draw"     : 0
        }

    def _getMinToken(self, board: TTTBoard):
        '''
        Returns the token of opponent from board
        '''
        tokens = board.getPlayerTokens()
        for token in tokens:
            if token != self.getToken():
                return token

    def _isTerminalState(self, board: TTTBoard):
        '''
        If terminal state, return result
        otherwise return None
        '''
        full = board.isFull()
        winner = board.checkForWinner()
        if full and winner is not None:
            return winner
        if full and winner is None:
            return "draw"
        return None

    def _miniMax(self, board: TTTBoard, depth: int, maximizing: bool):
        '''
        pseudo code : https://en.wikipedia.org/wiki/Minimax
        function minimax(node, depth, maximizingPlayer) is
            if depth = 0 or node is a terminal node then
                return the heuristic value of node
            if maximizingPlayer then
                value := −∞
                for each child of node do
                    value := max(value, minimax(child, depth − 1, FALSE))
                return value
            else (* minimizing player *)
                value := +∞
                for each child of node do
                    value := min(value, minimax(child, depth − 1, TRUE))
                return value
        '''
        # Check for terminal state and return reward if true
        check_term = self._isTerminalState(board)
        if check_term == "draw":
            return 0
        if check_term == self._token:
            return 1
        if check_term == "O":
            return -1

        moves     = board.getCurrentOpenPositions()
        min_token = self._getMinToken(board)
    
        if maximizing:
            value = -math.inf
            for move in moves:
                board.placeToken(move, self.getToken())
                value = max(value, self._miniMax(board, depth + 1, False))
                board.clearPosition(move)
                #if len(moves) <= 2: print("Move {} value {}".format(move, value))
            return value 
        else:
            value = math.inf
            for move in moves:
                board.placeToken(move, min_token)
                value = min(value, self._miniMax(board, depth + 1, True))
                board.clearPosition(move)
                #if len(moves) <= 2: print("Move {} value {}".format(move, value))
            return value 


    def passReward(self, reward: float, state_actions: list):
        pass

    def getMove(self, board: TTTBoard):
        best_score = -math.inf
        best_move  = None
        moves      = board.getCurrentOpenPositions()
        # for each available move, copy board, make move, get value from minimax function
        #if len(moves) == board.size():
        #    print("random move")
        #    return self.getRandomMove(board)
        for move in moves:
            board.placeToken(move, self.getToken())
            score = self._miniMax(board, 0, False)
            if score > best_score:
                best_score = score
                best_move  = move
            board.clearPosition(move)\
        return best_move



def main():
    """
    mini_max = TTTMiniMaxAgent('X')  
    player_1 = TTTQAgent('O') 

    player_2 = TTTRandomAgent('X')

    ttt_game     = TicTacToe(player_1, player_2)
    minimax_game = TicTacToe(mini_max, player_1)

    ttt_game.train(50000, show_results=True, p_1=player_1, p_2=player_2)
    player_2 = TTTQAgent('X')
    ttt_game  = TicTacToe(player_1, player_2)
    ttt_game.train(50000, show_results=True, p_1=player_1, p_2=player_2)

    minimax_game.test(50, show_results=True, verbose=True)
    

    

    
    for i in range(1000):
        print("| ---------- TRAINING ---------- |")
        ttt_game.train(100, p_2=True)
        print("Testing after training for {} games".format(i*100))
        ttt_game.test(100, show_results=True)
    """
    player_1 = TTTMiniMaxAgent('X')
    player_2 = TTTPlayer('O')
    ttt_game = TicTacToe(player_1, player_2)
    ttt_game.test(10, show_results=True, verbose=True)
    #for i in range(10000):
    #    print("Trained for {} games".format(i+1))
    #    ttt_game.train(1, p_1=True)
    #    ttt_game.test(1000, show_results=True)
    

if __name__ == '__main__':
    main()