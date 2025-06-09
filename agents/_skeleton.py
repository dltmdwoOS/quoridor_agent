from pathlib import Path
from random import choice
from time import time
from traceback import print_exc, format_exc
from typing import Tuple, List, Callable, Dict, Generator, Optional, Literal, Union

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

    def heuristic_search(self, board: GameBoard) -> List[Action]:
        """
        * Complete this function to answer the challenge PART I.

        This function uses heuristic search for finding the best route to the goal line.
        You have to return a list of action, which denotes the shortest actions toward the goal.

        RESTRICTIONS: USE one of the following algorithms or its variant.
        - Breadth-first search
        - Depth-first search
        - Uniform-cost search
        - Greedy Best-first search
        - A* search
        - IDA*
        - RBFS
        - SMA*

        :param board: The game board with initial game setup.
        :return: A list of actions.
        """
        raise NotImplementedError()

    def local_search(self, board: GameBoard, time_limit: float) -> List[BLOCK]:
        """
        * Complete this function to answer the challenge PART II.

        This function uses local search for finding the three best place of the fence.
        The system calls your algorithm multiple times, repeatedly.
        Each time, it provides new position of your pawn and asks your next decision
         until time limit is reached, or until you return a BLOCK action.

        Each time you have to decide one of the action.
        - If you want to look around neighborhood places, return MOVE action
        - If you decide to answer the best place, return BLOCK action
        * Note: you cannot move to the position that your opponent already occupied.

        You can use your heuristic search function, which is previously implemented, to compute the fitness score of each place.
        * Note that we will not provide any official fitness function here. The quality of your answer depends on the first part.

        RESTRICTIONS: USE one of the following algorithms or its variant.
        - Hill-climbing search and its variants
        - Simulated annealing and its variants
        - Tabu search and its variants
        - Greedy Best-first search
        - Local/stochastic beam search (note: parallel execution should be called as sequentially)
        - Evolutionary algorithms
        - Empirical/Stochastic gradient methods
        - Newton-Raphson method

        :param board: The game board with current state.
        :param time_limit: The time limit for the search. Datetime.now() should have lower timestamp value than this.
        :return: The list of three BLOCKs. That is, you should return [BLOCK(), BLOCK(), BLOCK()].
        """
        raise NotImplementedError()

    def belief_state_search(self, board: GameBoard, time_limit: float) -> List[Action]:
        """
        * Complete this function to answer the challenge PART III.

        This function uses belief state search for finding the best move for certain amount of time.
        The system calls your algorithm only once. Your algorithm should consider the time limit.

        You can use your heuristic search or local search function, which is previously implemented, to compute required information.

        RESTRICTIONS: USE one of the following algorithms or its variant.
        - AND-OR search and its variants
        - Heuristic/Uninformed search algorithms whose state is actually a belief state.
        - Online DFS algorithm, or other online variant of heuristic/uninformed search.
        - LRTA*

        :param board: The game board with initial game setup.
        :param time_limit: The time limit for the search. Datetime.now() should have lower timestamp value than this.
        :return: The next move.
        """
        raise NotImplementedError()

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
        raise NotImplementedError()
