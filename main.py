from numpy import *

marks = ['.', '○', '●', ' ']

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def get_size():
    while(True):
        x = int(input('X<< '))
        y = int(input('Y<< '))
        z = int(input('Z<< '))

        if x & 1 or y & 1 or z & 1:
            print('偶数にして')
        else:
            return Vector3(x, y, z)

class Game:
    class Board:
        class Cell:
            def __init__(self, coordinate):
                self.coordinate = coordinate

        def __init__(self, size):
            self.board = array([[[self.Cell(Vector3(x, y, z)) for x in range(size.x)] for y in range(size.y)] for z in range(size.z)])

        def at(self, coordinate):
            return self.board[coordinate.z][coordinate.y][coordinate.x]

        def print(self):
            pass

    def __init__(self, size):
        self.size = size
        self.board = self.Board(self.size)

if __name__ == '__main__':
    size = get_size()

    game = Game(size)
