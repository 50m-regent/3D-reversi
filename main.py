from numpy import *

marks = ['.', '○', '●']

class Game:
    class Board:
        def __init__(self, size):
            self.size = size
            
            self.board = [
                [
                    [
                        0 for z in range(self.size.z)
                    ] for y in range(self.size.y)
                ] for x in range(self.size.x)
            ]
            self.board[self.size.x // 2 - 1][self.size.y // 2 - 1][self.size.z // 2 - 1] = 1
            self.board[self.size.x // 2 - 1][self.size.y // 2 - 1][self.size.z // 2] = 2
            self.board[self.size.x // 2 - 1][self.size.y // 2][self.size.z // 2 - 1] = 2
            self.board[self.size.x // 2 - 1][self.size.y // 2][self.size.z // 2] = 1
            self.board[self.size.x // 2][self.size.y // 2 - 1][self.size.z // 2 - 1] = 2
            self.board[self.size.x // 2][self.size.y // 2 - 1][self.size.z // 2] = 1
            self.board[self.size.x // 2][self.size.y // 2][self.size.z // 2 - 1] = 1
            self.board[self.size.x // 2][self.size.y // 2][self.size.z // 2] = 2

        def print(self):
            def get_front():
                data = [
                    [
                        marks[0] for y in range(self.size.y)
                    ] for x in range(self.size.x)
                ]

                for x in range(self.size.x):
                    for y in range(self.size.y):
                        for z in range(self.size.z):
                            cell = self.board[x][y][z]
                            if cell != 0:
                                data[x][y] = marks[cell]
                                break
                
                return rot90(array(data))

            def get_back():
                data = [
                    [
                        marks[0] for y in range(self.size.y)
                    ] for x in range(self.size.x)
                ]

                for x in range(self.size.x):
                    for y in range(self.size.y):
                        for z in range(self.size.z):
                            cell = self.board[self.size.x - 1 - x][y][self.size.z - 1 - z]
                            if cell != 0:
                                data[x][y] = marks[cell]
                                break
                
                return rot90(array(data))

            def get_left():
                data = [
                    [
                        marks[0] for z in range(self.size.z)
                    ] for y in range(self.size.y)
                ]

                for y in range(self.size.y):
                    for z in range(self.size.z):
                        for x in range(self.size.x):
                            cell = self.board[x][y][self.size.z - 1 - z]
                            if cell != 0:
                                data[y][z] = marks[cell]
                                break
                
                return rot90(array(data), k=2)

            def get_right():
                data = [
                    [
                        marks[0] for z in range(self.size.z)
                    ] for y in range(self.size.y)
                ]

                for y in range(self.size.y):
                    for z in range(self.size.z):
                        for x in range(self.size.x):
                            cell = self.board[self.size.x - 1 - x][y][z]
                            if cell != 0:
                                data[y][z] = marks[cell]
                                break
                
                return rot90(array(data), k=2)

            def get_up():
                data = [
                    [
                        marks[0] for x in range(self.size.x)
                    ] for z in range(self.size.z)
                ]

                for z in range(self.size.z):
                    for x in range(self.size.x):
                        for y in range(self.size.y):
                            cell = self.board[x][y][z]
                            if cell != 0:
                                data[z][x] = marks[cell]
                                break

                return array(data)

            def get_down():
                data = [
                    [
                        marks[0] for x in range(self.size.x)
                    ] for z in range(self.size.z)
                ]

                for z in range(self.size.z):
                    for x in range(self.size.x):
                        for y in range(self.size.y):
                            cell = self.board[x][self.size.y - 1 - y][self.size.z - 1 - z]
                            if cell != 0:
                                data[z][x] = marks[cell]
                                break

                return array(data)

            front = get_front()
            back  = get_back()
            left  = get_left()
            right = get_right()
            up    = get_up()
            down  = get_down()
            
            left_margin  = array([
                [
                    ' ' for z in range(self.size.z)
                ] for z in range(self.size.z)
            ])
            right_margin = array([
                [
                    ' ' for i in range(self.size.x + self.size.z)
                ] for z in range(self.size.z)
            ])

            data = concatenate([
                concatenate([left_margin, up, right_margin], axis=1),
                concatenate([left, front, right, back], axis=1),
                concatenate([left_margin, down, right_margin], axis=1)
            ])

            for row in data:
                for cell in row:
                    print(cell, end = ' ')
                print()

    def __init__(self, size):
        self.board = self.Board(size)

    def print(self):
        self.board.print()

def get_board_size():
    class Vector3:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
    
    while(True):
        x = int(input('X<< '))
        y = int(input('Y<< '))
        z = int(input('Z<< '))
        
        if x & 1 or y & 1 or z & 1:
            print('Size must be even number!!!!!!!!!!')
        else:
            break

    return Vector3(x, y, z)

if __name__ == '__main__':
    game = Game(get_board_size())
    game.print()
