from random import randint, shuffle, sample


class Bag:

    def __init__(self):
        self.nums = sample(range(1, 91), 90)

    def next(self):
        if self.nums:
            return self.nums.pop()
        raise Exception('Мешок пуст!')

    def stats(self):
        print(f'В мешке {len(self.nums)} боченков.')

    def __str__(self):
        str_nums = ''
        for n in sorted(self.nums.copy()):
            str_nums += f'{n}, '
        return f'Всего {len(self.nums)} бочонков №№: {str_nums}'

    def __eq__(self, other):
        return sorted(self.nums) == sorted(other.nums)

    def __len__(self):
        return len(self.nums)


class Card:

    def __init__(self, name):
        self.player_name = name
        # генерация чисел для карточки
        self.card_nums = sample(range(1, 91), 15)
        # генерация мест для этих чисел на карточке
        self.place_idx = sample(range(0, 9), 5) + sample(range(9, 18), 5) + sample(range(18, 27), 5)
        # print(place_idx)

        # словарь {№места: число}
        self.card = {key: 0 for key in range(27)}
        for i in range(len(self.card_nums)):
            self.card[self.place_idx[i]] = self.card_nums[i]

    def modify(self, num):
        del_idx = self.place_idx[self.card_nums.index(num)]
        self.card[del_idx] = None

    def show(self):

        # печать карточки
        print(f'\n-{self.player_name}{"-" * (26 - len(self.player_name) - 1)}')
        for i in range(len(self.card)):
            if self.card[i] is None:
                print('--', end='')
            elif self.card[i] == 0:
                print('  ', end='')
            elif self.card[i] < 10:
                print(f' {self.card[i]}', end='')
            else:
                print(self.card[i], end='')
            print() if i + 1 in (9, 18, 27) else print(' ', end='')
        print('-' * 26, end='\n')

    def __str__(self):
        str_card = f'\n-{self.player_name}{"-" * (26 - len(self.player_name) - 1)}\n'
        for i in range(len(self.card)):
            if self.card[i] is None:
                str_card += '--'
            elif self.card[i] == 0:
                str_card += '  '
            elif self.card[i] < 10:
                str_card += f' {self.card[i]}'
            else:
                str_card += f'{self.card[i]}'
            str_card += '\n' if i + 1 in (9, 18, 27) else ' '
        str_card += '-' * 26 + '\n'
        return str_card

    def __eq__(self, other):
        return sorted(self.card_nums) == sorted(other.card_nums)

    def __len__(self):
        return len(self.card_nums)

class Computer:

    def __init__(self, name='Computer'):
        self.name = name
        self.card = Card(name)
        self.nums = self.card.card_nums.copy()
        self.is_winner = False

    def step(self, num):

        if num in self.card.card_nums:
            self.card.modify(num)
            self.nums.remove(num)
            self.is_winner = not self.nums

    def stats(self):
        print(f'{self.name}. Осталось {len(self.nums)} чисел : {self.nums}')

    def __str__(self):
        str_card = str(self.card)
        return str_card + f'Имя игрока: {self.name}\nОсталось {len(self.nums)} чисел : {sorted(self.nums)}'

    def __eq__(self, other):
        return (sorted(self.nums) == sorted(other.nums)) and (self.is_winner == other.is_winner)

    def __contains__(self, item):
        return True if self.name == item else False

    def __getitem__(self, item):
        return self.nums[item]

    def __len__(self):
        return len(self.nums)


class User(Computer):

    def __init__(self, name='User'):
        Computer.__init__(self, name)

        self.is_looser = False
        self.answers = ['y', 'n']

    def step(self, num):
        answer = input(f'{self.name}, зачеркнуть цифру? (y/n) ')
        while answer not in self.answers:
            answer = input('Не понял вас... Зачеркнуть цифру? (y/n) ')
        if answer == 'y':
            if num in self.card.card_nums:
                self.card.modify(num)
                self.nums.remove(num)
                self.is_winner = not self.nums
            else:
                self.is_looser = True
        elif answer == 'n':
            if num in self.card.card_nums:
                self.is_looser = True

    def __str__(self):
        str_card = str(self.card)
        return str_card + f'Имя игрока: {self.name}\nОсталось {len(self.nums)} чисел : {sorted(self.nums)}'

    def __eq__(self, other):
        return (sorted(self.nums) == sorted(other.nums)) and (self.is_winner == other.is_winner)

    def __contains__(self, item):
        return True if self.name == item else False


class Game:
    def __init__(self):
        self.num_users = 0
        self.num_compics = 0
        self.players = {}
        self.bag = Bag()
        self.winners = []
        self.losers = []

    def generate_players(self, num_compics, num_users):

        for i in range(num_compics):
            pl_name = f'compic-{i+1}'
            self.players[pl_name] = Computer(pl_name)

        for i in range(num_users):
            pl_name = f'user-{i+1}'
            self.players[pl_name] = User(pl_name)

    def run(self, num_compics, num_users):
        self.num_compics = num_compics
        self.num_users = num_users

        self.generate_players(num_compics, num_users)
        self.cards_show()

        while True:
            num = self.bag.next()

            print(f'Из мешка вынут боченок номер {num}!')

            self.step(num)

            if self.num_users == 0 and self.num_compics == 0:
                print('\nTHE GAME IS OVER == FINITA LA COMEDIA')
                break

            self.cards_show()
            self.stats_show()

            self.bag.stats()

            if self.check_winner():
                break
            else:
                print('Игра продолжается...\n')

    def step(self, num):
        for player in self.players.values():
            player.step(num)
            if isinstance(player, User):
                if player.is_looser:
                    print(f'\nСОЖАЛЕЮ, {player.name}, но ВЫ ПРОИГРАЛИ... Нужно быть внимательнее!')
                    self.num_users -= 1
                    # заносим лузеров в список для удаления из словаря игроков
                    self.losers.append(player)
                    # break
        # удаляем лузеров
        for loser in self.losers:
            self.players.pop(loser.name)
        # удаляем список лузеров, т.к. мы их только что удалили
        self.losers = []

    def cards_show(self):
        for player in self.players.values():
            player.card.show()

    def stats_show(self):
        for player in self.players.values():
            player.stats()

    def check_winner(self):

        # Составляем список победителей, если они есть
        for player in self.players.values():
            if player.is_winner:
                self.winners.append(player)

        if len(self.winners) > 1:
            print(f'\nНИЧЬЯ!!! Победили {[winner.name for winner in self.winners]}!')
            return True
        elif self.winners:
            print(f'ПОБЕДИЛ {self.winners[0].name}!')
            return True

        return False

    def __str__(self):
        str_resume = f'\nПАРАМЕТРЫ ИГРЫ:\nЧисло игроков: {self.num_users + self.num_compics}\n' \
                    f'- биологических: {self.num_users}\n- кремниевых: {self.num_compics}\n' \
                    f'Число боченков: {len(self.bag.nums)}\nНомеров в каждой карточке: {15}\n' \
                    f'Чило победителей: {len(self.winners)}\nИмена победителей: {self.winners}\n' \
                    f'Чило проигравших: {len(self.losers)}\nИмена проигравших: {self.losers}\n'

        return str_resume

    def __eq__(self, other):
        return (self.num_users == other.num_users) \
               and (self.num_compics == other.num_compics) \
               and (self.winners == other.winners) \
               and (self.losers == other.losers) \
               and (self.bag == other.bag) \
               and (self.players == other.players)

    def __len__(self):
        return len(self.players)


if __name__ == '__main__':
    import copy

    print('\nРаспечатываем объект класса Bag')
    bag = Bag()
    print(bag)

    print('\nРаспечатываем объект класса Card')
    card = Card('Ivan')
    print(card)

    print('\nРаспечатываем объект класса Computer')
    comp = Computer('Terminator')
    print(comp)

    print('\nРаспечатываем объект класса User')
    usr = User('Ванечка')
    print((usr))

    print('\nРаспечатываем объект класса Game')
    game = Game()
    print(game)

    # Проверка сравнения объектов класса Bag
    print('\nПроверка сравнения объектов класса Bag')

    bag1 = Bag()
    bag2 = Bag()
    print(bag1 == bag2)

    num3 = bag2.nums[3]
    bag2.nums[3] = 99
    print(bag1 == bag2)

    bag2.nums[3] = num3
    print(bag1 == bag2)

    # Проверка сравнения объектов класса Card
    print('\nПроверка сравнения объектов класса Card')

    card1 = Card('card1')
    card2 = Card('card1')
    card3 = copy.copy(card1)

    print(card1 == card2)
    print(card2 == card3)
    print(card3 == card1)

    # Проверка сравнения объектов класса Computer и User
    print('\nПроверка сравнения объектов класса Computer  и User')
    cmp1 = Computer('comp')
    cmp2 = Computer('comp')
    cmp3 = copy.copy(cmp1)

    usr1 = User('user')
    usr2 = User('user')
    usr3 = copy.copy(usr1)

    print(cmp1 == cmp2)
    print(cmp2 == cmp3)
    print(cmp3 == cmp1)

    print(usr1 == usr2)
    print(usr2 == usr3)
    print(usr3 == usr1)

    print(usr1 == cmp3)

    # Проверка сравнения объектов класса Game
    print('\nПроверка сравнения объектов класса Game')

    gam1 = Game()
    gam2 = Game()
    gam3 = copy.copy(gam1)

    print(gam1 == gam2)
    print(gam2 == gam3)
    print(gam3 == gam1)

    gam2.num_users = 6

    print(gam1 == gam2)
    print(gam2 == gam3)
    print(gam3 == gam1)

    # Проверка наличия игрока с данным именем в объекте класса User
    print('\nПроверка наличия игрока с данным именем в объекте класса User')

    user1 = User('Маняша')
    user2 = User('Ванюша')
    print('Маняша' in user1)
    print('Маняша' in user2)

    # Проверка наличия игрока с данным именем в объекте класса Computer
    print('\nПроверка наличия игрока с данным именем в объекте класса Computer')

    comp = Computer()
    print('Computer' in comp)

    # Проверка итерируемости списка незачеркнутых номеров в карточках игроков Computer и User
    print('\nПроверка итерируемости списка незачеркнутых номеров в карточках игроков Computer и User')

    usr = User()
    for num in usr:
        print(num)

    i = 5
    print(f'{i}-м числом на карточке {usr.name} является число {usr[i - 1]}')


    # Проверка длины объектов классов Bag, Card, Computer, User, Game
    print('\nПроверка длины объектов классов Bag, Card, Computer, User, Game')

    bag = Bag()
    card = Card('Игрок2')
    comp = Computer()
    user = User()
    game = Game()

    print(f'Длина объекта класса Bag = {len(bag)} боченков')
    print(f'Длина объекта класса Card = {len(card)} незачеркнутых чисел')
    print(f'Длина объекта класса Computer = {len(comp)} незачеркнутых чисел')
    print(f'Длина объекта класса User = {len(user)} незачеркнутых чисел')
    print(f'Длина объекта класса Game = {len(game)} игроков')