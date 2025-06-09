# Abstract Class annotations
import abc
# Logging method for board execution
import logging
# Library for OS environment
import sys
# Type definition of Python
from typing import Tuple, Literal

import pyquoridor.board
from pyquoridor.exceptions import InvalidFence

#: True if the program run with 'DEBUG' environment variable.
IS_DEBUG = '--debug' in sys.argv

# Maximum number of fences
FENCES_MAX = 10

class Action(abc.ABC):
    """
    Abstract class for action
    """

    #: [PRIVATE] Logger instance for Action's function calls
    _logger = logging.getLogger('Action')

    @abc.abstractmethod
    def __call__(self, board, avoid_check=False):
        """
        Executing/Simulating an action on a game board

        :param board: Game board to manipulate
        :param avoid_check: Check whether the game finished or not
        """
        raise NotImplementedError()


class MOVE(Action):
    """
    Move pawn to the specified direction.
    """

    def __init__(self, player: Literal['black', 'white'], position: Tuple[int, int]):
        """
        Action for moving pawn on the specified square.

        :param player: ID of the current player. black or white. (You can get this from board.get_player_index())
        :param position: Square to move pawn to.
        """
        self.player = player
        self.position = position

        assert self.player in ('black', 'white'), 'Player must be one of "black" or "white"'

    def __repr__(self):  # String representation for this
        return f'MOVE{self.position} of {self.player}'

    def __call__(self, board, avoid_check=False):
        if IS_DEBUG:  # Logging for debugging
            self._logger.debug(f'Calling {str(self)} action')

        # This can raise two exceptions: GameOver / InvalidMove
        # These two exceptions will be handled in the board.
        board._board.move_pawn(self.player, *self.position,
                               check_winner=not avoid_check, check_player=not avoid_check)


class BLOCK(Action):
    """
    Construct a fence
    """

    def __init__(self, player: Literal['black', 'white'], edge: Tuple[int, int],
                 orientation: Literal['horizontal', 'vertical']):
        """
        Action for constructing a fence at edge.

        :param player: ID of the current player. black or white. (You can get this from board.get_player_index())
        :param edge: The center coordinate of the edge, i.e., (row, col)
        :param orientation: 'horizontal' or 'vertical', Direction of the fence.
        """
        self.player = player
        self.edge = edge
        self.orientation = orientation[0]

        assert self.orientation in 'hv', 'Orientation must be one of "horizontal" or "vertical"'
        assert self.player in ('black', 'white'), 'Player must be one of "black" or "white"'

    def __repr__(self):  # String representation for this
        return f'BLOCK_{self.orientation}{self.edge} of player {self.player}'

    def __call__(self, board, avoid_check=False):
        if IS_DEBUG:  # Logging for debugging
            self._logger.debug(f'Calling BLOCK construction on edge {self.edge}.')

        assert board._board.fences_left[self.player] > 0, f'{self.player} has no fences left.'

        # This can raise two exceptions: GameOver / InvalidMove
        # These two exceptions will be handled in the board.
        board._board.place_fence(*self.edge, self.orientation, check_winner=not avoid_check)
        board._fences.append((self.edge, self.orientation))


# Export actions only
__all__ = ['Action', 'MOVE', 'BLOCK', 'FENCES_MAX']
