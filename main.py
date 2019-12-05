from numpy import *

alias = ['None', 'White', 'Black', 'Placable']
marks = [' ', '○', '●', '.']

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def get_size():
    while(True):
        print('Board Size')
        x = int(input('X<< '))
        y = int(input('Y<< '))
        z = int(input('Z<< '))

        if x & 1 or y & 1 or z & 1:
            print('Board size must be even number!!!')
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
            self.board = [[[self.Cell(Vector3(x, y, z)) for x in range(self.size.x)] for y in range(self.size.y)] for z in range(self.size.z)]
            self.set_piece()

        def set_piece(self):
            self.at(Vector3(self.size.x // 2, self.size.y // 2, self.size.z // 2)).team = 1
            self.at(Vector3(self.size.x // 2, self.size.y // 2, self.size.z // 2 - 1)).team = 2
            self.at(Vector3(self.size.x // 2, self.size.y // 2 - 1, self.size.z // 2)).team = 2
            self.at(Vector3(self.size.x // 2, self.size.y // 2 - 1, self.size.z // 2 - 1)).team = 1
            self.at(Vector3(self.size.x // 2 - 1, self.size.y // 2, self.size.z // 2)).team = 2
            self.at(Vector3(self.size.x // 2 - 1, self.size.y // 2, self.size.z // 2 - 1)).team = 1
            self.at(Vector3(self.size.x // 2 - 1, self.size.y // 2 - 1, self.size.z // 2)).team = 1
            self.at(Vector3(self.size.x // 2 - 1, self.size.y // 2 - 1, self.size.z // 2 - 1)).team = 2

        def at(self, coordinate):
            return self.board[coordinate.z][coordinate.y][coordinate.x]

        def out(self):
            left_margin  = array([[self.Cell() for z in range(self.size.z)] for zz in range(self.size.z)])
            right_margin = array([[self.Cell() for zx in range(self.size.z + self.size.x)] for z in range(self.size.z)])

            front = array([[self.Cell() for x in range(self.size.x)] for y in range(self.size.y)])
            back  = array([[self.Cell() for x in range(self.size.x)] for y in range(self.size.y)])
            for x in range(self.size.x):
                for y in range(self.size.x):
                    for z in range(self.size.z):
                        cell = self.at(Vector3(x, y, self.size.z - 1 - z))
                        if cell.team != 0:
                            front[y][x] = cell
                    for z in range(self.size.z):
                        cell = self.at(Vector3(self.size.x - 1 - x, y, z))
                        if cell.team != 0:
                            back[y][x] = cell

            left  = array([[self.Cell() for z in range(self.size.z)] for y in range(self.size.y)])
            right = array([[self.Cell() for z in range(self.size.z)] for y in range(self.size.y)])
            for z in range(self.size.z):
                for y in range(self.size.y):
                    for x in range(self.size.x):
                        cell = self.at(Vector3(self.size.x - 1 - x, y, self.size.z - 1 - z))
                        if cell.team != 0:
                            left[y][z] = cell
                    for x in range(self.size.x):
                        cell = self.at(Vector3(x, y, z))
                        if cell.team != 0:
                            right[y][z] = cell

            top    = array([[self.Cell() for x in range(self.size.x)] for z in range(self.size.z)])
            bottom = array([[self.Cell() for x in range(self.size.x)] for z in range(self.size.z)])
            for x in range(self.size.x):
                for z in range(self.size.z):
                    for y in range(self.size.y):
                        cell = self.at(Vector3(x, self.size.y - 1 - y, self.size.z - 1 - z))
                        if cell.team != 0:
                            top[z][x] = cell
                    for y in range(self.size.y):
                        cell = self.at(Vector3(x, y, z))
                        if cell.team != 0:
                            bottom[z][x] = cell

            return concatenate([
                concatenate([left_margin, top, right_margin], axis=1),
                concatenate([left, front, right, back], axis=1),
                concatenate([left_margin, bottom, right_margin], axis=1)
            ])

        def score(self):
            score = {'None': 0, 'White': 0, 'Black': 0, 'Placable': 0}
            for plane in self.board:
                for row in plane:
                    for cell in row:
                        score[alias[cell.team]] += 1
            
            return score

    def __init__(self, size):
        self.size = size
        self.board = self.Board(self.size)

    def out(self):
        data = self.board.out()
        for row in data:
            for cell in row:
                print(marks[cell.team], end=' ')
            print()

        score = self.board.score()
        print('White ' + str(score['White']) + ' : ' + str(score['Black']) + ' Black')

    def get_maneuver(self):
        print('Next Maneuver')

        while True:
            x = int(input('X<< '))
            y = int(input('Y<< '))
            z = int(input('Z<< '))
            x -= 1
            y -= 1
            z -= 1

            if self.board.at(Vector3(x, y, z)).team == -1:
                return Vector3(x, y, z)
            else:
                print('That cell is not placable!')

    def set_placable(self):
        count = 0

        return count

    def play(self, debug=False):
        turn = 1

        while True:
            turn = turn % 2 + 1
            placable_count = self.set_placable()

            if placable_count == 0:
                print('Pass')
                continue

            if debug:
                self.out()

            print(alias[turn] + "'s turn")
            maneuver = self.get_maneuver()

if __name__ == '__main__':
    size = get_size()

    game = Game(size)
    game.play(debug=True)
