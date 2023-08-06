from abc import ABC
from nerdchess.config import MOVE_REGEX, letterlist, numbers


class Move(ABC):
    """
    Represents a move in a game of chess.

    Parameters:
    move(String): A string that's tested with the regex '[a-h][1-8][a-h][1-8]'

    Attributes:
    text(String): String representation of the move r'[a-h][1-8][a-h][1-8]'
    origin(String): String representation of the origin square
    destination(String): String representation of the destination square
    horizontal(int): Amount of horizontal steps in the move
    vertical(int): Amount of vertical steps in the move
    indices(dict): Origin/destination letter(x)/number(y) mapped to their list
                   position
    """

    def __init__(self, move):
        valid_move = MOVE_REGEX.match(move)
        if not valid_move:
            raise ValueError('Invalid move')

        self.text = move
        self.origin = move[:2]
        self.destination = move[2:]
        self.indices = {
            'or': {
                'x': letterlist.index(self.origin[0]),
                'y': numbers.index(int(self.origin[1]))
            },
            'dest': {
                'x': letterlist.index(self.destination[0]),
                'y': numbers.index(int(self.destination[1]))
            }
        }
        (self.horizontal,
         self.vertical) = self.get_steps()

    @classmethod
    def from_position(cls, position, steps):
        """Create a move based on the current position and steps (hori/verti).

        Parameters:
            position(String): The current position (eg. a1)
            steps(tuple(int, int)): The steps taken in the move

        Returns:
            Move: A new move instance
        """
        (letter_steps, number_steps) = steps
        current_letter_index = letterlist.index(position[0])
        current_number_index = numbers.index(int(position[1]))

        new_letter_index = current_letter_index + letter_steps
        new_number_index = current_number_index + number_steps

        if new_letter_index >= 0 and new_number_index >= 0:
            new_letter = letterlist[new_letter_index]
            new_number = numbers[new_number_index]
        else:
            return None

        move = "{}{}{}".format(position, new_letter, new_number)
        return cls(move)

    # TODO Clean up this mess of a function
    def squares_between(self):
        """ Return the squares between the origin and destination. """
        squares = []

        if self.horizontal == 1 or self.vertical == 1:
            return squares

        if self.horizontal == -1 or self.vertical == -1:
            return squares

        if self.is_diagonal():
            steps = 1 if self.horizontal > 0 else -1
            if self.vertical < 0 and steps == 1:
                v_steps = -1
            elif self.vertical > 0 and steps == -1:
                v_steps = -1
            else:
                v_steps = 1

            try:
                for i in range(steps, self.horizontal, steps):
                    step_index_x = self.indices['or']['x'] + i
                    step_index_y = self.indices['or']['y'] + (i * v_steps)

                    if step_index_x < 0 or step_index_y < 0:
                        continue

                    letter = letterlist[step_index_x]
                    number = numbers[step_index_y]
                    square = f"{letter}{number}"
                    squares.append(square)
            except IndexError:
                pass
        elif self.is_horizontal():
            steps = 1 if self.horizontal > 0 else -1
            for i in range(steps, self.horizontal, steps):
                letter = letterlist[self.indices['or']['x'] + i]
                number = self.origin[1]
                square = f"{letter}{number}"
                squares.append(square)
        elif self.is_vertical():
            steps = 1 if self.vertical > 0 else -1
            for i in range(steps, self.vertical, steps):
                letter = self.origin[0]
                number = numbers[self.indices['or']['y'] + i]
                square = f"{letter}{number}"
                squares.append(square)

        return squares

    def is_diagonal(self):
        """ Is the move diagonal? """
        if self.horizontal == 0 or self.vertical == 0:
            return False
        if not abs(self.horizontal) == abs(self.vertical):
            return False
        return True

    def is_horizontal(self):
        """ Is the move horizontal (only)? """
        if self.horizontal == 0:
            return False
        if self.vertical != 0:
            return False
        return True

    def is_vertical(self):
        """ Is the move vertical (only)? """
        if self.vertical == 0:
            return False
        if self.horizontal != 0:
            return False
        return True

    def get_steps(self):
        """ Return the horizontal/vertical steps of the move. """
        horizontal_steps = self.indices['dest']['x'] - \
            self.indices['or']['x']
        vertical_steps = self.indices['dest']['y'] - \
            self.indices['or']['y']

        return (horizontal_steps, vertical_steps)

    def __eq__(self, item):
        """ Describes how to compare a Move. """
        if isinstance(item, Move):
            return self.text == item.text
        try:
            return self.text == str(item)
        except TypeError:
            return NotImplemented

    def __str__(self):
        """ String representation of a Move. """
        return self.text
