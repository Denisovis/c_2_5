# from random import randint, randbytes


class SeaBattleExeptions(Exception):
    pass


class BoardOutExeption(SeaBattleExeptions):
    def __str__(self):
        return "Вы стреляете за пределы поля!"


class ShotTwiseExeption(SeaBattleExeptions):
    def __str__(self):
        return "Вы сюда уже стреляли!"


class ShipOutExeption(SeaBattleExeptions):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

    def __str__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:
    def __init__(self, length, head, horizontal):
        self.length = length
        self.head = head
        self.horizontal = horizontal
        self.hp = length

    @property
    def dots(self):
        result = []
        for _ in range(self.length):
            current_dot_x = self.head.x
            current_dot_y = self.head.y
            if self.horizontal:
                current_dot_y += _
            else:
                current_dot_x += _
            result.append(Dot(current_dot_x, current_dot_y))
        return result


class Board:
    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid

        self.field = [['0']*size for _ in range(size)]
        self.ships = []
        self.busy = []
        self.shoten_dots = []
        self.ship_count = 0

    def add_ship(self, ship):
        for d in ship.dots:
            if d in self.busy or self.out(d):
                raise ShipOutExeption

        for d in ship.dots:
            self.field[d.y][d.x] = "■"
            self.busy.append(d)
        self.ships.append(ship)
        self.ship_count += 1

    def out(self, dot):
        return not (0 <= dot.x < self.size and 0 <= dot.y < self.size)

    def contour(self, ship, show=False):
        contour_cords = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for cx, cy in contour_cords:
                c_dot = Dot(d.x + cx, d.y + cy)
                if c_dot not in self.busy and not self.out(c_dot):
                    if show:
                        self.field[c_dot.y][c_dot.x] = '~'
                    self.busy.append(c_dot)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutExeption('Вы стреляете за пределы поля')
        if dot in self.shoten_dots:
            raise ShotTwiseExeption('Вы сюда уже стреляли')
        self.busy.append(dot)
        self.shoten_dots.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                self.field[dot.y][dot.x] = 'X'
                ship.hp -= 1
                if not ship.hp:
                    print('Корабль потоплен!')
                    self.contour(ship, True)
                else:
                    print('Корабль повреждён!')
                return True
            else:
                self.field[dot.y][dot.x] = '.'
                print('Мимо')
                return False


    def __str__(self):
        _out = ''
        for _ in range(self.size + 1):
            _out += f'{_} | '
        for i, j in enumerate(self.field):
            _out += f'\n{i + 1} | ' + ' | '.join(j) + ' |'
        if self.hid:
            _out = _out.replace('■', '0')
        return _out


class Player:
    def __init__(self):
        self.board = Board(6)
        self.enemy_board = Board(6)

    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                target = self.ask()
                if not self.enemy_board.shot(target):
                    return True
                else:
                    return False
            except SeaBattleExeptions as e:
                print(e)
                return True





if __name__ == '__main__':
    # Тесты и прочий не нужный код
    myBoard = Board(9)
    myShip = Ship(2, Dot(0, 0), False)
    print(myShip.dots)
    myBoard.add_ship(myShip)
    myBoard.hid = False
    print(myBoard)

    for _ in range(5):
        try:
            print(myBoard.shot(Dot(int(input('x ')) - 1, int(input('y ')) - 1)))
            print(myBoard)
        except SeaBattleExeptions as e:
            print(e)
    print(myBoard.__dict__)
    print(myShip.__dict__)


