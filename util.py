def print_board(board):
    """
    Return current game board.
    @source: pyquoridor.utils
    """
    nx = len(board.board)
    ny = len(board.board)
    output = ''

    for y in range(ny - 1, -1, -1):
        row_fence_str = '  '

        row_str = str(y) + ' :'
        for x in range(nx):
            # Horizontal fences
            # down_fence = square.get_fence('up')
            if board.fence_center_grid[(y, x - 1)]:
                row_fence_str += '*'
            else:
                row_fence_str += ' '

            if board.horizontal_fence_grid[(y, x)]:  # down_fence is None:
                row_fence_str += '---'
            else:
                row_fence_str += '. .'

            # Vertical fences
            # right_fence = square.get_fence('right')
            if board.vertical_fence_grid[(y, x)]:
                right_str = '|'
            else:
                right_str = '·'

            # print(':   ' * nx + ':')
            content = f'   '
            if board[y, x].is_busy():
                pawn_color = board[y, x].pawn.color[0].upper()
                content = f' {pawn_color} '
            row_str += f'{content}{right_str}'
        output += row_fence_str + '\n'
        # print('  ' + ' ···' * nx)
        output += row_str + '\n'
        # Fence: print('|   ' * nx + '|')
    output += '  ' + (' ···' * nx) + '\n'
    output += '  ' + ''.join([f'  {i} ' for i in range(nx)])

    return output
