from ticTacToe import TTTPlayer
from ticTacToe import TTTBoard
from ticTacToe import TicTacToe
from ticTacToe import TTTRandomAgent
import pprint
import random

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
        self._epsilon     = 0.1
        self._epsi_decay  = 0.993
        self._epsi_min    = 0.005
        self._alpha       = 0.9
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
            return max_value #self.getRandomMove(board)
        except:
            self._addHash(board_hash, board.validMovesForHash(board_hash))
            return self.getRandomMove(board)

    def _getMaxQFromHash(self, state_hash: str):
        try:
            moves = self._q_table[state_hash]
            #print("Moves:", moves)
            return max([moves[key] for key in moves.keys()])
        except:
            return self._init_q_val

    def _addHash(self, board_hash: str, available_moves: list):
        '''
        '''
        #print("adding : {}".format(board_hash))
        state_action_values = { }
        for move in available_moves:
            state_action_values[move] = self._init_q_val
        self._q_table[board_hash] = state_action_values

    def _addReward(self, reward: float, action: int, state_hash: str):
        '''
        Add reward to state's action 
        '''
        #print("hash:", state_hash)
        #print("action:", action)
        #print("added reward:", reward)
        #input()
        try:
            self._q_table[state_hash][action] += reward
        except:
            self._addHash(state_hash, TTTBoard.validMovesForHash(state_hash))
            self._q_table[state_hash][action] += reward

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
        #print("alpha:", self._alpha)
        #print("disc :", self._discount)
        #print("maxa :", max_next_q)
        #print("maxc :", self._getQValue(state_hash, action))
        return self._alpha * (self._discount * max_next_q - self._getQValue(state_hash, action))

    def setEpsilonDecay(self, decay: float):
        self._epsi_decay = decay

    def trainModel(self, train: bool):
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
            #print("\nQ-Table before: ", self._q_table)
            prev_reward = reward
            prev_hash   = state_actions[-2][0]
            prev_action = state_actions[-2][1] 
            self._addReward(reward, prev_action, prev_hash)
            #print(prev_hash)
            #input()

            max_next_q = self._getMaxQFromHash(prev_hash)

            i = len(state_actions) - 3 
            # Reverse list from second to last element to beginning
            while i >= 0 :
                curr_hash   = state_actions[i][0]
                curr_action = state_actions[i][1]
                curr_reward = self._calcReward(curr_hash, curr_action, max_next_q)
                #print(curr_hash, "reward: ", curr_reward)
                self._addReward(curr_reward, curr_action, curr_hash)

                prev_reward = curr_reward
                prev_hash   = curr_hash
                prev_action = curr_action
                max_next_q  = self._getMaxQFromHash(prev_hash)
                #print(prev_hash)
                #input()
                #print("action: ", state_actions[i][1]) 
                i -= 1

            # Decay exploration rate
            #if self._epsilon >= self._epsi_min:
             #   self._epsilon *= self._epsi_decay


            #print("\nQ-Table after: ", self._q_table)
            #print("State Actions: ", state_actions)
            #print("Reward: ", reward)
            #input()

    def getQTable(self):
        return self._q_table

    def getMove(self, board: TTTBoard):
        # Policy :
        # get hash value of current borad state
        # get possible moves from board state
        # choose move with highest value
        # if multiple moves have the same value, pick randomly
        #if random.uniform(0, 1) > self._epsilon:
        return self._getMaxQMove(board)
        # Else take a random action
        #else:
        #    return self.getRandomMove(board)
        #return self.getRandomMove(board)

    def getRandomMove(self, board: TTTBoard):
        '''
        Returns randomly chosen move
        '''
        valid_moves = board.getCurrentOpenPositions()
        rand_idx    = random.randint(0, len(valid_moves) - 1)
        #print("Valid Moves: {}".format(valid_moves))
        return valid_moves[rand_idx]




import operator
def main():
    '''
    For debugging
    '''
    player_1 = TTTQAgent('X')    
    player_2 = TTTQAgent('O')
    ttt_game = TicTacToe(player_1, player_2)

    #for x in range(10000):
    #    ttt_game.playGame()
    #    if not x % 10000:
    #        print("After game {} :".format(x))
    #        ttt_game.displayResults()

    player_1.trainModel(True)

    for x in range(20000):
        ttt_game.playGame()
        if not x % 10000:
            print("Learning Opponent game {} :".format(x))
            ttt_game.displayResults()

    player_1.trainModel(False)
    player_2.trainModel(True)

    for x in range(20000):
        ttt_game.playGame()
        if not x % 10000:
            print("Learning Opponent game {} :".format(x))
            ttt_game.displayResults()

    player_1.trainModel(True)
    player_2.trainModel(False)

    for x in range(20000):
        ttt_game.playGame()
        if not x % 10000:
            print("Learning Opponent game {} :".format(x))
            ttt_game.displayResults()

    player_1.trainModel(False)
    player_2.trainModel(True)

    for x in range(20000):
        ttt_game.playGame()
        if not x % 10000:
            print("Learning Opponent game {} :".format(x))
            ttt_game.displayResults()

    player_1.trainModel(True)
    player_2.trainModel(False)

    for x in range(20000):
        ttt_game.playGame()
        if not x % 10000:
            print("Learning Opponent game {} :".format(x))
            ttt_game.displayResults()

    human_player = TTTPlayer('O')
    new_game = TicTacToe(player_1, human_player, True)

    for x in range(20):
        new_game.playGame()
    new_game.displayResults()


    '''
    for i in range(10000):
        ttt_game.playGame()
        #pprint.pprint(player_1.getQTable())
        #pprint.pprint(player_2.getQTable())
        #input("Play next game")
    
    #pprint.pprint(player_1.getQTable())
    #ttt_game.displayWinners()
    print("After 10000 games : ")
    ttt_game.displayResults()
    '''


if __name__ == '__main__':
    main()