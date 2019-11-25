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
        print('-' * 26, end='\n\n')

# Родительский класс - воможно потом
# class Player:


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


class User(Computer):

    def __init__(self, name='User'):
        Computer.__init__(self, name)

        self.is_looser = False
        self.answers = ['y', 'n']

    def step(self, num):
        answer = input('Зачеркнуть цифру? (y/n) ')
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


class Game:
    def __init__(self):
        # self.players = []
        self.user = User()
        self.compic = Computer()
        self.bag = Bag()

    # def new_player(self):
    #     self.players.append()
    #     pass

    def run(self):

        self.cards_show()

        while True:
            num = self.bag.next()

            print(f'Из мешка вынут боченок номер {num}!')

            self.step(num)

            if self.user.is_looser:
                print('\nСОЖАЛЕЮ, но ВЫ ПРОИГРАЛИ... Нужно быть внимательнее!')
                break

            self.cards_show()
            self.user.stats()
            self.compic.stats()
            self.bag.stats()

            # game.check_winner(players)

            if self.check_winner():
                break
            else:
                print('Игра продолжается...\n')

    def step(self, num):
        self.user.step(num)
        self.compic.step(num)

    def cards_show(self):
        self.user.card.show()
        self.compic.card.show()

    def check_winner(self):
        if self.user.is_winner and self.compic.is_winner:
            print('\nНИЧЬЯ!!!')
            return True
        elif self.user.is_winner:
            print('\nВЫ ПОБЕДИТЕЛЬ!')
            return True
        elif self.compic.is_winner:
            print('\nКОМПИК ПОБЕДИТЕЛЬ!')
            return True

        return False

        # for player in players:
        #     if player.is_winner():
        #         return True
        # pass
        # Если оба - ничья
        # Если никто - "игра продожается"
        # Если кто-то - объявляем победителя и игра завершается
        # Если кто пользователь проиграл, то сообщение и игра завершается


if __name__ == '__main__':
    pass
