from numpy import *

alias = ['None', 'White', 'Black', 'Placable']
marks = [' ', '○', '●', '.']

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def add(self, delta):
        return Vector3(
            self.x + delta.x,
            self.y + delta.y,
            self.z + delta.z
        )

class Game:
    class Board:
        class Cell:
            def __init__(self, coordinate=Vector3(0, 0, 0), team=0):
                self.coordinate = coordinate
                self.team       = team

        def __init__(self, size):
            def set_piece():
                self.at(Vector3(self.size.x // 2, self.size.y // 2, self.size.z // 2)).team = 1
                self.at(Vector3(self.size.x // 2, self.size.y // 2, self.size.z // 2 - 1)).team = 2
                self.at(Vector3(self.size.x // 2, self.size.y // 2 - 1, self.size.z // 2)).team = 2
                self.at(Vector3(self.size.x // 2, self.size.y // 2 - 1, self.size.z // 2 - 1)).team = 1
                self.at(Vector3(self.size.x // 2 - 1, self.size.y // 2, self.size.z // 2)).team = 2
                self.at(Vector3(self.size.x // 2 - 1, self.size.y // 2, self.size.z // 2 - 1)).team = 1
                self.at(Vector3(self.size.x // 2 - 1, self.size.y // 2 - 1, self.size.z // 2)).team = 1
                self.at(Vector3(self.size.x // 2 - 1, self.size.y // 2 - 1, self.size.z // 2 - 1)).team = 2

            self.size  = size
            self.board = [[[self.Cell(Vector3(x, y, z)) for x in range(self.size.x)] for y in range(self.size.y)] for z in range(self.size.z)]
            set_piece()

        def at(self, coordinate):
            try:
                return self.board[coordinate.z][coordinate.y][coordinate.x]
            except:
                return self.Cell(team=-1)

        def out(self):
            left_margin  = array([[self.Cell() for z in range(self.size.z)] for zz in range(self.size.z)])
            right_margin = array([[self.Cell() for zx in range(self.size.z + self.size.x)] for z in range(self.size.z)])

            front = array([[self.Cell() for x in range(self.size.x)] for y in range(self.size.y)])
            back  = array([[self.Cell() for x in range(self.size.x)] for y in range(self.size.y)])
            for x in range(self.size.x):
                for y in range(self.size.x):
                    for z in range(self.size.z):
                        cell = self.at(Vector3(x, y, self.size.z - 1 - z))
                        if front[y][x].team == 0 or cell.team not in (0, 3):
                            front[y][x] = cell
                    for z in range(self.size.z):
                        cell = self.at(Vector3(self.size.x - 1 - x, y, z))
                        if back[y][x].team == 0 or cell.team not in (0, 3):
                            back[y][x] = cell

            left  = array([[self.Cell() for z in range(self.size.z)] for y in range(self.size.y)])
            right = array([[self.Cell() for z in range(self.size.z)] for y in range(self.size.y)])
            for z in range(self.size.z):
                for y in range(self.size.y):
                    for x in range(self.size.x):
                        cell = self.at(Vector3(self.size.x - 1 - x, y, self.size.z - 1 - z))
                        if left[y][z].team == 0 or cell.team not in (0, 3):
                            left[y][z] = cell
                    for x in range(self.size.x):
                        cell = self.at(Vector3(x, y, z))
                        if right[y][z].team == 0 or cell.team not in (0, 3):
                            right[y][z] = cell

            top    = array([[self.Cell() for x in range(self.size.x)] for z in range(self.size.z)])
            bottom = array([[self.Cell() for x in range(self.size.x)] for z in range(self.size.z)])
            for x in range(self.size.x):
                for z in range(self.size.z):
                    for y in range(self.size.y):
                        cell = self.at(Vector3(x, self.size.y - 1 - y, self.size.z - 1 - z))
                        if top[z][x].team == 0 or cell.team not in (0, 3):
                            top[z][x] = cell
                    for y in range(self.size.y):
                        cell = self.at(Vector3(x, y, z))
                        if bottom[z][x].team == 0 or cell.team not in (0, 3):
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

    def play(self, debug=False):
        turn = 1

        def search(now, delta, flip=False):
            if self.board.at(now).team in (-1, 0):
                return False
            if self.board.at(now).team == turn:
                return True
            
            if flip:
                self.board.at(now).team = turn
                
            return search(now.add(delta), delta)

        def set_placable():
            def is_placable(coordinate):
                
                deltas = [
                    Vector3(-1, -1, -1),
                    Vector3(-1, -1, 0),
                    Vector3(-1, -1, 1),
                    Vector3(-1, 0, -1),
                    Vector3(-1, 0, 0),
                    Vector3(-1, 0, 1),
                    Vector3(-1, 1, -1),
                    Vector3(-1, 1, 0),
                    Vector3(-1, 1, 1),
                    Vector3(0, -1, -1),
                    Vector3(0, -1, 0),
                    Vector3(0, -1, 1),
                    Vector3(0, 0, -1),
                    Vector3(0, 0, 1),
                    Vector3(0, 1, -1),
                    Vector3(0, 1, 0),
                    Vector3(0, 1, 1),
                    Vector3(1, -1, -1),
                    Vector3(1, -1, 0),
                    Vector3(1, -1, 1),
                    Vector3(1, 0, -1),
                    Vector3(1, 0, 0),
                    Vector3(1, 0, 1),
                    Vector3(1, 1, -1),
                    Vector3(1, 1, 0),
                    Vector3(1, 1, 1)
                ]

                for delta in deltas:
                    if self.board.at(coordinate).team == 0 and self.board.at(coordinate.add(delta)).team == turn % 2 + 1 and search(coordinate.add(delta).add(delta), delta):
                        self.board.at(coordinate).team = 3
                        print(coordinate.x, coordinate.y, coordinate.z)
                        return True
                
                return False

            count = 0

            for x in range(self.size.x):
                for y in range(self.size.y):
                    for z in range(self.size.z):
                        if self.board.at(Vector3(x, y, z)).team == 3:
                            self.board.at(Vector3(x, y, z)).team = 0
                        if is_placable(Vector3(x, y, z)):
                            count += 1

            return count

        def out():
            data = self.board.out()
            for row in data:
                for cell in row:
                    print(marks[cell.team], end=' ')
                print()

            score = self.board.score()
            print('White ' + str(score['White']) + ' : ' + str(score['Black']) + ' Black')

        def get_maneuver():
            print('Next Maneuver')

            while True:
                x = int(input('X<< '))
                y = int(input('Y<< '))
                z = int(input('Z<< '))
                x -= 1
                y -= 1
                z -= 1

                if self.board.at(Vector3(x, y, z)).team == 3:
                    return Vector3(x, y, z)
                else:
                    print('That cell is not placable!')

        def flip():
            deltas = [
                Vector3(-1, -1, -1),
                Vector3(-1, -1, 0),
                Vector3(-1, -1, 1),
                Vector3(-1, 0, -1),
                Vector3(-1, 0, 0),
                Vector3(-1, 0, 1),
                Vector3(-1, 1, -1),
                Vector3(-1, 1, 0),
                Vector3(-1, 1, 1),
                Vector3(0, -1, -1),
                Vector3(0, -1, 0),
                Vector3(0, -1, 1),
                Vector3(0, 0, -1),
                Vector3(0, 0, 1),
                Vector3(0, 1, -1),
                Vector3(0, 1, 0),
                Vector3(0, 1, 1),
                Vector3(1, -1, -1),
                Vector3(1, -1, 0),
                Vector3(1, -1, 1),
                Vector3(1, 0, -1),
                Vector3(1, 0, 0),
                Vector3(1, 0, 1),
                Vector3(1, 1, -1),
                Vector3(1, 1, 0),
                Vector3(1, 1, 1)
            ]

            self.board.at(self.maneuver).team = turn

            for delta in deltas:
                if self.board.at(self.maneuver.add(delta)).team == turn % 2 + 1 and search(self.maneuver.add(delta).add(delta), delta):
                    search(self.maneuver.add(delta), delta, flip=True)

        while True:
            turn = turn % 2 + 1
            placable_count = set_placable()

            if placable_count == 0:
                print('Pass')
                continue

            if debug:
                out()

            print(alias[turn] + "'s turn")
            self.maneuver = get_maneuver()

            flip()

if __name__ == '__main__':
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

    size = get_size()

    game = Game(size)
    game.play(debug=True)
