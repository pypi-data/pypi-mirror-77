import copy
from nerdchess.config import colors, letters
from nerdchess.boardmove import BoardMove, CastleSide
from nerdchess.pieces import King


class Board():
    """
    Represents a board in a game of chess.

    {
        a: {
            1: (Square),
            2: (Square),
            etc...
        },
        b: {
            1: (Square),
            2: (Square),
            etc...
        }
        etc...
    }

    Attributes:
        letters(list): The letters of a board
        numbers(list): The numbers of a board
        squares(dict): A dict of letters containing numbers with squares

    """

    def __init__(self):
        self.letters = [i.value for i in letters]
        self.numbers = range(1, 9)
        self.squares = {}
        self.create_board()

    @classmethod
    def piece_list(cls, square_dict, color=None):
        """Generator to get the current pieces on the board as a list.

        Parameters:
            square_dict: The dictionary of squares to get the list from
        """
        for v in square_dict.values():
            if isinstance(v, dict):
                yield from cls.piece_list(v, color)
            else:
                if v.occupant:
                    if color:
                        if v.occupant.color == color:
                            yield v.occupant
                        else:
                            pass
                    else:
                        yield v.occupant
                else:
                    pass

    def matrix(self):
        """ Returns a matrix of the board represented as list. """
        matrix = []

        for i in reversed(self.numbers):
            row = []
            row.append(str(i))

            for letter in self.letters:
                row.append(str(self.squares[letter][i]))

            matrix.append(row)

        last_row = []
        last_row.append(' X ')
        for letter in self.letters:
            last_row.append("_{}_".format(letter))

        matrix.append(last_row)

        return matrix

    def setup_board(self, game_pieces, pawns):
        """ Set up the pieces and pawns in one go. """
        self.setup_pieces(game_pieces)
        self.setup_pawns(pawns)

    def place_piece(self, piece, position):
        """
        Place a piece or pawn on the board.
        Mostly used for testing setups.
        """
        letter = position[0]
        number = int(position[1])
        self.squares[letter][number].occupant = piece
        piece.position = position

    def setup_pieces(self, game_pieces):
        """Sets up the pieces on the board.

        Parameters:
            game_pieces: A list of pieces to set up
        """
        for piece in game_pieces:
            row = 1 if piece.color == colors.WHITE else 8

            for letter in self.letters:
                square = self.squares[letter][row]
                if (square.selector in piece.start_position()
                        and not square.occupant):
                    piece.position = square.selector
                    square.occupant = piece
                    break

    def setup_pawns(self, pawns):
        """Sets up the pawns on the board.

        Parameters:
            pawns: A list of pawns to set up
        """
        for pawn in pawns:
            row = 2 if pawn.color == colors.WHITE else 7

            for letter in self.letters:
                square = self.squares[letter][row]

                if not square.occupant:
                    square.occupant = pawn
                    pawn.position = square.selector
                    break

    def create_board(self):
        """ Create the board. """
        for letter in self.letters:
            self.squares[letter] = {}

            for number in self.numbers:
                selector = "{}{}".format(letter, number)
                self.squares[letter][number] = Square(selector)

    # TODO write a test to see if bishops can't check through pawns
    def is_check(self, color=None):
        """Is one of the kings in check?

        Parameters:
            color(optional): The color to check for

        Returns:
            color: The color of the king that is in check or False
        """
        pieces = list(self.piece_list(self.squares, color))
        for piece in pieces:
            moves = [BoardMove(i.text) for i in piece.allowed_moves()]
            for move in moves:
                if not move:
                    continue

                (origin,
                 destination) = move.get_origin_destination(self)

                if not destination.occupant:
                    continue

                if (isinstance(destination.occupant, King) and
                        destination.occupant.color != origin.occupant.color):
                    return destination.occupant.color

        return False

    def is_checkmate(self):
        """Is one of the kings in checkmate?

        Returns:
            color: Color of the king in mate or False
        """
        check = self.is_check()
        if not check:
            return False

        pieces = list(self.piece_list(self.squares, check))
        moves = []
        for i in pieces:
            moves = moves + i.allowed_moves()

        boardmoves = [BoardMove(i.text) for i in moves]

        for move in boardmoves:
            valid_move = move.process(self)
            if valid_move:
                if not valid_move.is_check(check):
                    return False

        return check

    def new_board(self, move):
        """Create a new board from a supplied move.

        This does not do any explicit validation on the move.

        Parameters:
            move: The move to process

        Returns:
            newboard: The new board
        """
        newboard = copy.deepcopy(self)
        move = BoardMove(move.text)

        (origin, destination) = move.get_origin_destination(newboard)
        piece = origin.occupant

        origin.occupant = None
        if destination.occupant:
            destination.occupant.captured = True
        destination.occupant = piece
        piece.position = destination.selector

        return newboard

    def castle(self, side, color):
        """ Perform castling on a board.

        Parameters:
            side: The side to castle to
            color: The color performing the castle

        Returns:
            newboard: A new board with the processed move
        """
        newboard = copy.deepcopy(self)

        if color == colors.WHITE:
            kingsquare = newboard.squares['e'][1]
            if side == CastleSide.QUEEN:
                rooksquare = newboard.squares['a'][1]
            else:
                rooksquare = newboard.squares['h'][1]
        else:
            kingsquare = newboard.squares['e'][8]
            if side == CastleSide.QUEEN:
                rooksquare = newboard.squares['a'][8]
            else:
                rooksquare = newboard.squares['h'][8]

        kchar = 'c' if side == CastleSide.QUEEN else 'g'
        rchar = 'd' if side == CastleSide.QUEEN else 'f'
        kint = 1 if color == colors.WHITE else 8
        rint = 1 if color == colors.WHITE else 8
        king_dest = newboard.squares[kchar][kint]
        rook_dest = newboard.squares[rchar][rint]

        king = kingsquare.occupant
        rook = rooksquare.occupant
        kingsquare.occupant = None
        rooksquare.occupant = None

        king_dest.occupant = king
        rook_dest.occupant = rook
        king.position = king_dest.selector
        rook.position = rook_dest.selector

        return newboard


class Square():
    """Represents a square on a chessboard.

    Parameters:
        selector: A selector of the square (eg. a1)
        occupant: Usually a piece or pawn, needs to have __str__
    """

    def __init__(self, selector, occupant=None):
        self.selector = selector
        self.occupant = occupant

    def __str__(self):
        """ String representation of a square. """
        if self.occupant:
            return "[{}]".format(str(self.occupant))
        else:
            return '[ ]'
