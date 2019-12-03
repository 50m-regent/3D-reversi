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
            def __init__(self, coordinate=Vector3(0, 0, 0), team=0):
                self.coordinate = coordinate
                self.team       = team

        def __init__(self, size):
            self.size  = size
            self.board = array([[[self.Cell(Vector3(x, y, z)) for x in range(self.size.x)] for y in range(self.size.y)] for z in range(self.size.z)])

        def at(self, coordinate):
            return self.board[coordinate.z][coordinate.y][coordinate.x]

        def print(self):
            left_margin  = array([[self.Cell(team=-1) for z in range(self.size.z)] for zz in range(self.size.z)])
            right_margin = array([[self.Cell(team=-1) for zx in range(self.size.z + self.size.x)] for z in range(self.size.z)])

            front = array([[self.board.at(Vector3(x, y, 0)) for x in range(self.size.x)] for y in range(self.size.y)])
            back  = array([[self.board.at(Vector3(x, y, -1))]])

            pass

    def __init__(self, size):
        self.size = size
        self.board = self.Board(self.size)

if __name__ == '__main__':
    size = get_size()

    game = Game(size)
