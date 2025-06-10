from pathlib import Path
from random import choice
from typing import List, Literal, Union

from action import *
from board import GameBoard


class Agent:  # Do not change the name of this class!
    """
    An agent class
    """

    # Do not modify this.
    name = Path(__file__).stem

    # Do not change the constructor argument!
    def __init__(self, player: Literal['white', 'black']):
        """
        Initialize the agent

        :param player: Player label for this agent. White or Black
        """
        self.player = player

    def adversarial_search(self, board: GameBoard, time_limit: float) -> Action:
        """
        * Complete this function to answer the challenge PART IV.

        This function uses adversarial search to win the game.
        The system calls your algorithm whenever your turn arrives.
        Each time, it provides new position of your pawn and asks your next decision until time limit is reached.

        You can use your search function, which is previously implemented, to compute relevant information.

        RESTRICTIONS: USE one of the following algorithms or its variant.
        - Minimax algorithm, H-minimax algorithm, and Expectminimax algorithm
        - RBFS search
        - Alpha-beta search and heuristic version of it.
        - Pure Monte-Carlo search
        - Monte-Carlo Tree Search and its variants
        - Minimax search with belief states
        - Alpha-beta search with belief states

        :param board: The game board with current state.
        :param time_limit: The time limit for the search. Datetime.now() should have lower timestamp value than this.
        :return: The next move.
        """

        target_row = 8 if self.player == 'white' else 0
        oppo_row, oppo_col = board.get_position('white' if self.player == 'black' else 'black')

        fence_actions = [BLOCK(self.player, *f)
                         for f in board.get_applicable_fences(self.player)
                         if abs(f[0][0] - oppo_row) < 2 and abs(f[0][1] - oppo_col) < 2]
        move_actions = [MOVE(self.player, m)
                        for m in board.get_applicable_moves(self.player)]

        move_heuristic = [abs(m.position[0] - target_row) for m in move_actions]
        row_minimize = min(move_heuristic)
        move_actions = [move
                        for move, heuristic in zip(move_actions, move_heuristic)
                        if heuristic == row_minimize] # Only keep moves that minimize the row distance to the target

        if board.number_of_fences_left(self.player):
            actions = fence_actions + move_actions
        else:
            actions = move_actions
        action = choice(actions)

        return action

