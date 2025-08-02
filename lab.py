"""
6.101 Lab:
Mines
"""
#!/usr/bin/env python3

# import typing  # optional import
# import pprint  # optional import
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    keys = ("board", "dimensions", "state", "visible")
    # ^ Uses only default game keys. If you modify this you will need
    # to update the docstrings in other functions!
    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(nrows, ncolumns, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mines (list): List of mines, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    return new_game_nd((nrows,ncolumns),mines)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mines (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one mine
    is visible on the board after digging (i.e. game['visible'][mine_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    mine) and no mines are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing', 'all_True': 1, 'victory':5}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing', 'all_True': 1, 'victory':5}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    """
    return dig_nd(game, (row,col))


def render_2d_locations(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored
    and all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = {'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}
    >>> render_2d_locations(game, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations(game, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, all_visible)
    
def render_handle_row(row):
    """
    for all_visible, returns the render friendly list of cells

    args: 
        row: given row to convert

    returns: new row render friendly
    """
    returnable = []
    for cell in row:
        returnable.append(render_value(cell))
    return returnable

def not_vis_render_handle_row(row, visible):
    """
    for not all_visible, returns the render friendly list of cells

    args: 
        row: given row to convert
        visible: list of visibility for each square

    returns: new row render friendly
    """
    returnable = []
    for num in range(len(row)):
        vis=visible[num]
        if vis:
            returnable.append(render_value(row[num]))
        else:
            returnable.append('_')
    return returnable

def render_value(input):
    """
    returns a value for an input that is render friendly

    args:
        input: . or num

    returns: ' ' for 0, string of everything else
    """
    if input == 0:
        return ' '
    return str(input)

def render_2d_board(game, all_visible=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    array_board = render_2d_locations(game, all_visible)
    result_string = ''
    for row in array_board:
        for cell in row:
            result_string += cell
        result_string += '\n'
    if len(result_string)>=2:
        return result_string[:len(result_string)-1]
    return result_string


# N-D IMPLEMENTATION


def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]

    for each dimension, for loop until the dimension, and then if the type is not
    int, then go further in
    """
    
    #[3,4,5,6]

    board = blank_board(0, list(dimensions))
    visible = blank_board(False, list(dimensions))
    board = insert_mines(board, mines, dimensions)
    mult = 1
    for num in dimensions:
        mult = mult*num
    all_but_mines = mult-len(mines)
    return {'board': board, 'dimensions': dimensions, 'state': "ongoing", 'visible': visible,
            'all_True': 0, 'victory': all_but_mines}

def blank_board(val, temp):
    """
    creates a blank board with a given value

    args:
        val: to set all the blank spaces to
        temp: dimensions to make of a blank board

    returns: a blank board of nd array
    """
    if len(temp) ==1:
        return [val for _ in range(temp[0])]
    return [blank_board(val, temp[1:]) for _ in range(temp[0])]

def increment(loc, inner_board):
    """
    increments a given location on the board

    args:
        loc: the location to increment
        inner_board: the board that the loc maps in
    """
    cell_or_row = inner_board
    for i in range(len(loc)-1):
        cell_or_row = cell_or_row[loc[i]]
    try:
        cell_or_row[loc[-1]] = cell_or_row[loc[-1]]+1
    except TypeError:
        pass

def create_neighbor_array(dimensions, original):
    """
    creates all possibilities of adjacent cells relative to the original

    args:
        dimensions: the dimensions of the board
        original: the original cell to make neighbors around

    returns: set of tuple locs
    """
    def helper(dimensions):
        num_dimensions = len(dimensions)
        if num_dimensions ==1:
            return [[1,],[-1,],[0,]]
        remainder = helper(dimensions[1:])
        result = []
        for neighbor in remainder:
            result.append([1,] + neighbor)
            result.append([-1,] + neighbor)
            result.append([0,] + neighbor)
        return result
    adding = helper(dimensions)
    adding.remove([0 for _ in range(len(original))])
    result = set()
    for add in adding:
        neighbor = [original[i] + add[i] for i in range(len(original))]
        valid = {0<=neighbor[i]<dimensions[i] for i in range(len(original))}
        if False in valid:
            continue
        else:
            result.add(tuple(neighbor))
    return result

def add_neighbors(mine, inner_board,dimensions):
    """
    calls increment on the real neighbor values

    args:
        mine: the mine location
        inner_board: the board where the mine maps in
        dimensions: dimensions of the board
    """
    neighbors = create_neighbor_array(list(dimensions[:]), mine)
    for n in neighbors:
        increment(n,inner_board)

def insert_mines(inner_board, inner_mines,dimensions):
    """
    inserts mines into the board and calls add neighbors to change the numbers

    args:
        inner_board: the board where the mine maps in
        dimensions: dimensions of the board
        inner_mines: list of tuple mine locations
    
    returns: updated board
    """
    for mine in inner_mines:
        cell_or_row = inner_board
        for locnum in range(len(mine)-1):
            cell_or_row = cell_or_row[mine[locnum]]
        cell_or_row[mine[-1]] = '.'
        add_neighbors(mine, inner_board, dimensions)
    return inner_board

def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    mine.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one mine is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a mine) and no mines are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing',
    ...      'all_True': 1, 'victory': 13}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing',
    ...      'all_True': 1, 'victory': 13}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    #return num of squares revealed
    #if not ongoing, return 0
    #if mine visible, then state = defeat
    #if no safe covered, then state = victory

    #check state first
    def helper(current):
        if game['state'] != 'ongoing':
            return 0
        if not get_vis(game['visible'], current):
            row = game['board']
            for rownum in range(len(current)-1):
                row = row[current[rownum]]
            loc = current[-1]
            val = row[loc]
            set_vis(game, current)
            if val == '.':
                game['state'] = 'defeat'
                return 1
            elif val != 0:
                return 1
            #['.', 2, '.', 1, 0, 0, 1, '.', 2, '.']
            #[F,   T,  F,  T, F, F, F,  F,  F,  F]
            #dig(game, (4,)) == 3, giving 1
            else:
                neighbors = create_neighbor_array(game['dimensions'], current)
                counter = 1
                for n in neighbors:
                    if not get_vis(game['visible'], n):
                        counter+=helper(n)
                return counter
        return 0
    returnable = helper(coordinates)
    check_victory(game)
    return returnable

def check_victory(game):
    """
    checks if the number of visible is equal to the number needed for victory

    args:
        game: game that is being checked for victory
    """
    if game['state'] != 'defeat' and game['all_True'] == game['victory']:
        game['state'] = 'victory'

def get_vis(visible, coordinates):
    """
    gets the visibility at a given point

    args:
        visible: visible array
        coordinates: location we are checking for visibility
    
    return:
        True or False for visible
    """
    vis = visible
    for visnum in range(len(coordinates)):
        vis = vis[coordinates[visnum]]
    return vis

def set_vis(game, coordinates, val = True):
    """
    sets the visibility at a given location

    args:
        game: game where we are setting visibility
        coordinates: coordinates to set visibility at
        val: standard for True, what we are setting it to
    """
    vis = game['visible']
    for visnum in range(len(coordinates)-1):
        vis = vis[coordinates[visnum]]
    game['all_True'] +=1
    vis[coordinates[-1]] = val

def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  The game['visible'] array indicates which squares should be
    visible.  If all_visible is True (the default is False), the game['visible']
    array is ignored and all cells are shown.

    Args:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    board_copy = copy_board(game['board'],list(game['dimensions']))
    if not all_visible:
        locs = all_possible_locs(game['dimensions'])
        for loc in locs:
            vis = get_vis(game['visible'], loc)
            if not vis:
                pointer = board_copy
                for i in range(len(loc)-1):
                    pointer = pointer[loc[i]]
                pointer[loc[-1]] = '_'
    return board_copy

def all_possible_locs(dimensions):
    """
    returns all the possible locations for a given board

    args:
        dimensions: dimensions of the board
    
    returns: set of tuple locs
    """
    def helper(dimensions):
        num_dimensions = len(dimensions)
        if num_dimensions ==1:
            return [[i] for i in range(dimensions[0])]
        remainder = helper(dimensions[1:])
        result = []
        current = dimensions[0]
        for poss in remainder:
            for i in range(current):
                result.append([i]+poss)
        return result
    returnable = set()
    locs = helper(dimensions)
    for loc in locs:
        returnable.add(tuple(loc))
    return returnable

def copy_board(board, dimensions):
    """
    copies the board given that all_visible is true

    args:
        board: board to copy
        dimensions: dimensions of given board

    returns: nd array of string values
    """
    if len(dimensions) == 1:
        result = []
        for i in range(dimensions[0]):
            if board[i] != 0:
                result.append(str(board[i]))
            else:
                result.append(' ')
        return result
    return [copy_board(board[i], dimensions[1:]) for i in range(dimensions[0])]


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
