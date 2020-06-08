import random
import numpy as np

'''
Board Class for TicTacToe Game
'''
class TTTBoard:

    def __init__(self):
        self._rows  = 3
        self._cols  = 3 
        self._board = np.zeros(self._rows * self._cols, dtype=int)
        self._player_tokens = { }
        #self._board = [
        #    0, 1, 2,
        #    3, 4, 5,
        #    6, 7, 8
        #]

    @staticmethod
    def validMovesForHash(board_hash: str):
        '''
        Returns a list of open positions on board given a hash
        string of the board
        '''
        open_positions = []
        for idx in range(len(board_hash)):
            if board_hash[idx] == '0':
                open_positions.append(idx)
        return open_positions

    def _inBounds(self, position: int):
        '''
        Checks that given position is in bounds of game
        '''
        if position >= 0 and position <= 8:
            return True
        else:
            return False

    def _getPlayerToken(self, player_value: int):
        '''
        Returns token of player given their numeric value
        '''
        return self._player_tokens[player_value]

    def _getPlayerNum(self, token: str):
        '''
        Returns the numeric value of given token
        '''
        for key in self._player_tokens.keys():
            if self._player_tokens[key] == token:
                return key
        return None

    def getCurrentOpenPositions(self):
        '''
        Returns a list of open positions on current board
        '''
        open_positions = []
        for idx in range(self._board.shape[0]):
            if not self._board[idx]:
                open_positions.append(idx)
        return open_positions

    def addPlayer(self, player_token: str):
        '''
        Create hash using player token to access numeric version
        '''
        key_count = len(self._player_tokens.keys())
        self._player_tokens[key_count + 1] = player_token

    def boardState(self):
        '''
        Returns copy of the current board state
        '''
        return self._board.copy()

    def reset(self):
        '''
        Reset board to original state
        '''
        self._board = np.zeros(self._rows * self._cols, dtype=int)

    def display(self):
        '''
        Print current state of board to the terminal
        '''
        print()
        for row in range(self._rows):
            for col in range(self._cols):
                curr_val = self._board[(row * self._cols) + col]
                if not curr_val: print(" {} ".format((row * self._cols) + col), end="")
                else: print(" {} ".format(self._getPlayerToken(curr_val)), end="")
                if col < (self._cols - 1): print("|", end="")
            if row < (self._rows - 1): print("\n", "-" * (3 * self._cols), "-" * (self._cols - 1), sep="")
        print("\n")

    def checkForWinner(self):
        '''
        Checks the tokens in each column row and diagonal
        '''
        # Check columns
        if self._board[0] == self._board[3] and self._board[3] == self._board[6] and self._board[0]: return self._getPlayerToken(self._board[0])
        if self._board[1] == self._board[4] and self._board[4] == self._board[7] and self._board[1]: return self._getPlayerToken(self._board[1])
        if self._board[2] == self._board[5] and self._board[5] == self._board[8] and self._board[2]: return self._getPlayerToken(self._board[2])
        # Check rows
        if self._board[0] == self._board[1] and self._board[1] == self._board[2] and self._board[0]: return self._getPlayerToken(self._board[0])
        if self._board[3] == self._board[4] and self._board[4] == self._board[5] and self._board[3]: return self._getPlayerToken(self._board[3])
        if self._board[6] == self._board[7] and self._board[7] == self._board[8] and self._board[6]: return self._getPlayerToken(self._board[6])
        # Check diagonals
        if self._board[0] == self._board[4] and self._board[4] == self._board[8] and self._board[0]: return self._getPlayerToken(self._board[0])
        if self._board[2] == self._board[4] and self._board[4] == self._board[6] and self._board[2]: return self._getPlayerToken(self._board[2])

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
        if a positions board value is equal to zero
        '''
        if not self._board[position]:
            return True
        return False

    def placeToken(self, position: int, token: str):
        '''
        Places a token on the board if position is in correct range
        and the position is available
        '''
        player_num = self._getPlayerNum(token)
        if self.isValidMove(position) and player_num is not None:
            self._board[position] = player_num
            return True
        else: return False

    def isValidMove(self, position: int):
        '''
        Ensures the position is available and the position is within
        the bounds of the game board
        '''
        if self._inBounds(position) and self.positionAvailable(position): return True
        else: return False

    def getHash(self):
        '''
        Returns the hash value for current board state
        Hash value is the string of values at each position :
        i.e. empty board (3x3) = "000000000" 
        - empty = 0
        - p_1   = 1
        - p_2   = 2
        '''        
        board    = [str(val) for val in self._board]
        hash_str = "".join(board)
        return hash_str


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

    def passReward(self, reward: float, state_actions: list):
        pass

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
Always chooses random move
'''
class TTTRandomAgent(TTTPlayer):

    def getMove(self, board: TTTBoard):
        return self.getRandomMove(board)

    def getRandomMove(self, board: TTTBoard):
        '''
        Returns randomly chosen move
        '''
        valid_moves = board.getCurrentOpenPositions()
        rand_idx    = random.randint(0, len(valid_moves) - 1)
        #print("Valid Moves: {}".format(valid_moves))
        return valid_moves[rand_idx]


'''
Class to run a game between two players
'''
class TicTacToe:

    def __init__(self, p_1: TTTPlayer, p_2: TTTPlayer, display: bool = False):
        '''
        _results : all actions and board states of each game
        '''
        self._board   = TTTBoard()
        self._players = [{
            "player"       : p_1,
            "player_num"   : 1,
            "state_actions": []
        },
        {
            "player"       : p_2,
            "player_num"   : 2,
            "state_actions": []
        }
        ]
        self._results = []
        self._display = display
        self._addPlayers()

    def _addPlayers(self):
        '''
        Adds each player to game
        '''
        for player in self._players:
            self._board.addPlayer(player["player"].getToken())

    def _getNextPlayer(self, current_player: int):
        '''
        Returns the next player
        '''
        if current_player == 1: return 0
        else: return 1

    def _clearStateActions(self):
        '''
        Clear state action list for each player
        '''
        for player in self._players:
            player["state_actions"].clear()

    def shufflePlayers(self):
        '''
        Shuffle the order of the players
        '''
        random.shuffle(self._players)

    def displayWinners(self):
        '''
        Displays win results for each game
        '''
        print("\tWinner\n")
        for game in self._results:
            print("g_{}:\t{}".format(game["game_num"], game["winner"]))
        print()
    
    def displayResults(self):
        '''
        Displays the percent win of each player
        '''
        # reorder players list to ensure p_1 is first in list
        players = []
        if self._players[0]["player_num"] == 1:
            players.append(self._players[0])
            players.append(self._players[1])
        else:
            players.append(self._players[1])
            players.append(self._players[0])

        total_games   = len(self._results)
        player_1_wins = 0
        player_2_wins = 0
        draws         = 0
        for game in self._results:
            result = game["winner"]
            if result == "draw":
                draws += 1
            elif result == players[0]["player"].getToken():
                player_1_wins += 1
            else:
                player_2_wins += 1
        print("Player 1 : {}%".format(int(100*(player_1_wins/total_games))))
        print("Player 2 : {}%".format(int(100*(player_2_wins/total_games))))
        print("Draws    : {}%".format(int(100*(draws/total_games))))
        print()


    def rerunGame(self, game_num):
        '''
        Displays each board state from game number
        '''
        pass
    
    def getCurrBoardHash(self):
        '''
        Returns the current hash value of the board
        '''
        return self._board.getHash()

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
        if self._display: 
            self._board.display()
            print("Board Hash : {}".format(self.getCurrBoardHash()))
        game_data = {
            "board_states": [],
            "board_hashes": [],
            "winner"      : "",
            "game_num"    : 0
        }
        # game loop
        while not game_over:
            
            # get active player move
            player_input = self._players[curr_player]["player"].getMove(self._board)
            self._players[curr_player]["state_actions"].append((self._board.getHash(), player_input))
            # place token on board
            self._players[curr_player]["player"].placeToken(self._board, player_input)
            # check for winner
            winner = self._board.checkForWinner()
            if winner is not None:
                # game over : winner
                # add final state to state actions
                self._players[0]["state_actions"].append((self._board.getHash(), -1))
                self._players[1]["state_actions"].append((self._board.getHash(), -1))
                game_data["winner"] = winner
                for player in self._players:
                    if player["player"].getToken() == winner:
                        player["player"].passReward(1, player["state_actions"])
                    else:
                        player["player"].passReward(-1, player["state_actions"])
                if self._display: print("\nGame Over: Winner player token {}".format(winner))
                break
            # check for draw
            if self._board.isFull():
                # game over : draw
                # add final state to state actions
                self._players[0]["state_actions"].append((self._board.getHash(), -1))
                self._players[1]["state_actions"].append((self._board.getHash(), -1))
                game_data["winner"] = "draw"
                for player in self._players:
                    player["player"].passReward(0, player["state_actions"])
                if self._display: print("\nGame Over : Draw")
                break
            # switch player
            curr_player = self._getNextPlayer(curr_player)
            if self._display: 
                self._board.display()
                print("Board Hash : {}".format(self.getCurrBoardHash()))
        # append final board state and hash to game data
        game_data["board_states"].append(self._board.boardState())
        #game_data["board_hash"].append(self._board.getHash())
        game_data["game_num"] = len(self._results) + 1
        # append game data to results memeber
        self._results.append(game_data)
        self._clearStateActions()
        if self._display: 
            self._board.display()
            print("Board Hash : {}".format(self.getCurrBoardHash()))
    

def main():
    board = TTTBoard()
    board.getHash()


if __name__ == "__main__":
    main()