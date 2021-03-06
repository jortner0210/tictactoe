from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
import random
import pprint
import copy
import time
from tqdm import tqdm

'''
Board Class for TicTacToe Game
'''
class TTTBoard:

    def __init__(self):
        '''
        _player_tokens : { 
            1: "X", 
            2: "O", ...
        }
        '''
        self._rows  = 3
        self._cols  = 3 
        self._board = np.zeros(self._rows * self._cols, dtype=int)
        self._player_tokens = { }

    @staticmethod
    def validMovesForHash(board_hash: str):
        '''
        Returns a list of open positions on board given a board state hash
        '''
        open_positions = []
        for idx in range(len(board_hash)):
            if board_hash[idx] == '0':
                open_positions.append(idx)
        return open_positions

    def _inBounds(self, position: int):
        '''
        Checks if a position is within bounds of board
        '''
        if position >= 0 and position < (self._rows * self._cols): return True
        else: return False

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
            if self._player_tokens[key] == token: return key
        return None

    def size(self):
        '''
        Returns the size of the board
        '''
        return (self._rows * self._cols)

    def getPlayerTokens(self):
        '''
        Returns list of all player tokens
        '''
        return [self._player_tokens[key] for key in self._player_tokens.keys()]

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
        Add player to _player_tokens dictionary
        '''
        key_count = len(self._player_tokens.keys())
        self._player_tokens[key_count + 1] = player_token

    def copy(self):
        '''
        Returns copy of the current board state
        '''
        return copy.deepcopy(self)

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
        for i in range(9):
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
        if self._inBounds(position) and not self._board[position]: return True
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

    def clearPosition(self, position: int):
        '''
        Removes token from given postiion
        '''
        if self._inBounds(position): self._board[position] = 0

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
class TTTPlayer(ABC):

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

    def getRandomMove(self, board: TTTBoard):
        '''
        Returns randomly chosen move
        '''
        valid_moves = board.getCurrentOpenPositions()
        rand_idx    = random.randint(0, len(valid_moves) - 1)
        return valid_moves[rand_idx]

    @abstractmethod
    def passReward(self, reward: float, state_actions: list):
        pass

    @abstractmethod
    def getMove(self, board: TTTBoard):
        pass


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

    def _runGames(self, num_games: int, show_game: bool = False, show_results: bool = False,
                  train_p_1: bool = False, train_p_2: bool = False):
        '''
        Disable agent training and play through a number of games
        '''
        player_1 = [p["player"] for p in self._players if p["player_num"] == 1][0]
        player_2 = [p["player"] for p in self._players if p["player_num"] == 2][0]

        results = []
        # win percent for each batch of tests
        p_1_results   = []
        p_2_results   = []
        draw_results  = []

        mod = 1
        if num_games > 20: mod = num_games / 20
        
        self._display = show_game
        for game in tqdm(range(num_games)):
            # try to set agent to train - some agents are not trainable
            if train_p_1:
                try: player_1.trainAgent(True)
                except: pass
            if train_p_2:
                try: player_2.trainAgent(True)
                except: pass
            # run game
            game_results = self.playGame()
            game_results["game_num"] = len(results) + 1
            results.append(game_results)
            # run 500 tests if show_results argument is True
            if show_results and not (game + 1) % mod:
                test_results = self.test(500)
                p_1_wins = 0
                p_2_wins = 0
                draws    = 0
                for x in range(len(test_results)):
                    game = test_results[x]
                    if game["winner"] == player_1.getToken():
                        p_1_wins += 1
                    elif game["winner"] == "draw":
                        draws += 1
                    else:
                        p_2_wins += 1
                p_1_results.append(p_1_wins/len(test_results))
                p_2_results.append(p_2_wins/len(test_results))
                draw_results.append(draws/len(test_results))

        if show_results: self.graphRewards(p_1_results, p_2_results, draw_results, x_scale=mod)
        self._display = False
        return results

    def _shufflePlayers(self):
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

    def graphRewards(self, p_1: list, p_2: list, draws: list, x_scale: int = 1):
        '''
        Graphs the accumulated rewards of each game
        '''
        x = [(x + 1) * x_scale for x in range(len(p_1))]
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
        ax1.set_title("Player 1")
        ax2.set_title("Player 2")
        ax3.set_title("Draws")
        ax1.plot(x, p_1, "tab:blue")
        ax2.plot(x, p_2, "tab:red")
        ax3.plot(x, draws, "tab:green")
        fig.text(0.5, 0.04, "Games Trained", ha="center", va="center")
        fig.text(0.06, 0.5, "Win Rate - 500 Games", ha="center", va="center", rotation="vertical")     
        plt.show()
    
    @staticmethod
    def displayResults(self, results_struct: list):
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

        total_games   = len(results_struct)
        player_1_wins = 0
        player_2_wins = 0
        draws         = 0
        for game in results_struct:
            result = game["winner"]
            if result == "draw":
                draws += 1
            elif result == players[0]["player"].getToken():
                player_1_wins += 1
            else:
                player_2_wins += 1
        print("Games    : {}".format(total_games))
        print("Player 1 : {}%".format(int(100*(player_1_wins/total_games))))
        print("Player 2 : {}%".format(int(100*(player_2_wins/total_games))))
        print("Draws    : {}%".format(int(100*(draws/total_games))))
        print()
    
    def getCurrBoardHash(self):
        '''
        Returns the current hash value of the board
        '''
        return self._board.getHash()

    def test(self, num_games: int, show_results: bool = False, show_game: bool = False):
        '''
        Disable agent training and play through a number of games
        '''       
        #return self._runGames(False, num_games, show_game=show_game, show_results=show_results, p_1=True, p_2=True, test=False)
        player_1 = [p["player"] for p in self._players if p["player_num"] == 1][0]
        player_2 = [p["player"] for p in self._players if p["player_num"] == 2][0]

        results = []
        if show_game: self._display = True
        for game in range(num_games):
            try: player_1.trainAgent(False)
            except: pass
            try: player_2.trainAgent(False)
            except: pass
            game_results = self.playGame()
            game_results["game_num"] = len(results) + 1
            results.append(game_results)
        self._display = False
        return results

    def train(self, num_games: int, show_results: bool = False, show_game: bool = False, train_p_1: bool = False, train_p_2: bool = False):
        '''
        Enable training for players and run
        '''
        return self._runGames(num_games, show_game=show_game, show_results=show_results, train_p_1=train_p_1, train_p_2=train_p_2)
        
    def playGame(self):
        '''
        Play through game
        Current play is denoted by 0 or 1 - position is _players array
        Players are shuffled before the start of each game
        '''
        self._board.reset()
        self._shufflePlayers()
        game_over   = False
        curr_player = 0
        if self._display: 
            print("\n| ---------- GAME START ---------- |")
            self._board.display()

        game_data = {
            "board_states": [],
            "board_hashes": [],
            "winner"      : "",
            "game_num"    : 0
        }
        # game loop
        while not game_over:
            # get active player move
            active_player = self._players[curr_player]["player"]
            player_move   = active_player.getMove(self._board)
            # pass game states to data and player
            curr_hash = self._board.getHash()
            self._players[curr_player]["state_actions"].append((curr_hash, player_move))
            game_data["board_states"].append(copy.deepcopy(self._board))
            game_data["board_hashes"].append(curr_hash)
            # place token on board
            active_player.placeToken(self._board, player_move)
            if self._display: 
                print("Player {} placed token on position {}".format(active_player.getToken(), player_move))   
                self._board.display()
            # check for winner
            winner = self._board.checkForWinner()
            if winner is not None:
                # game over : winner
                game_data["winner"] = winner
                #self._players[0]["state_actions"].append((self._board.getHash(), -1))
                #self._players[1]["state_actions"].append((self._board.getHash(), -1))
                for player in self._players:
                    if player["player"].getToken() == winner:
                        player["player"].passReward(1, player["state_actions"])
                    else:
                        player["player"].passReward(-1, player["state_actions"])
                if self._display: print("Game Over: Winner player token {}".format(winner))
                break
            # check for draw
            if self._board.isFull():
                #self._players[0]["state_actions"].append((self._board.getHash(), -1))
                #self._players[1]["state_actions"].append((self._board.getHash(), -1))
                # game over : draw
                game_data["winner"] = "draw"
                for player in self._players:
                    player["player"].passReward(0, player["state_actions"])
                if self._display: print("Game Over : Draw")
                break
            # switch player
            curr_player = self._getNextPlayer(curr_player)
        # append final board state and hash to game data
        # add final state to state actions
        curr_hash = self._board.getHash()
        game_data["board_states"].append(self._board.copy())
        game_data["board_hashes"].append(curr_hash)
        #self._players[0]["state_actions"].append((curr_hash, -1))
        #self._players[1]["state_actions"].append((curr_hash, -1))

        self._clearStateActions()
        return game_data