from random import randint, shuffle, sample

# # генерация чисел для карточки
# card_nums = sample(range(1, 91), 15)
# # генерация мест для этих чисел на карточке
# place_idx = sample(range(0, 9), 5) + sample(range(9, 18), 5) + sample(range(18, 27), 5)
# print(place_idx)
#
# # словарь {№места: число}
# card = {key: 0 for key in range(27)}
# for i in range(len(card_nums)):
#     card[place_idx[i]] = card_nums[i]
#
# # печать карточки
# print('-' * 26)
# for i in range(len(card)):
#     if card[i] == 0:
#         print('  ', end='')
#     elif card[i] < 10:
#         print(f' {card[i]}', end='')
#     else:
#         print(card[i], end='')
#     print() if i + 1 in (9, 18, 27) else print(' ', end='')
# print('-' * 26, end='\n\n')


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
        print(f'-{self.player_name}{"-" * (26 - len(self.player_name) - 1)}')
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


# class Player:
#
#     def __init__(self):
#         self.card = Card()
#         self.nums = self.card.card.values()
#         self.answers = ['y', 'n']
#
#     def step(self, num):
#         answer = input('Зачеркнуть цифру? (y/n) ')
#         while answer not in self.answers:
#             answer = input('Не понял вас... Зачеркнуть цифру? (y/n) ')
#         if answer == 'y':
#             if num in self.card.card_nums:
#                 card.modify(num)
#                 self.nums = self.nums.remove(num)
#             else:
#                 return False
#         elif answer == 'n':
#             return False if num in self.card.card_nums else True
#
#     def is_winner(self):
#         # если список номеров пуст, то возвращает True, иначе False
#         return not self.nums


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


class User:

    def __init__(self, name='User'):
        self.name = name
        self.card = Card(name)
        self.nums = self.card.card_nums.copy()
        self.is_winner = False

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

    def stats(self):
        print(f'{self.name}. Осталось {len(self.nums)} чисел : {self.nums}')


class Game:
    def __init__(self):
        self.players = []
        pass

    def new_player(self):
        self.players.append()
        pass

    def check_winner(self, players):
        for player in players:
            if player.is_winner():
                return True
        pass
        # Если оба - ничья
        # Если никто - "игра продожается"
        # Если кто-то - объявляем победителя и игра завершается
        # Если кто пользователь проиграл, то сообщение и игра завершается


players = []

game = Game()
user = User()
compic = Computer()
players.append(user)

user.card.show()
compic.card.show()

bag = Bag()

while True:
    num = bag.next()

    print(f'Из мешка вынут боченок номер {num}!')

    user.step(num)
    compic.step(num)

    if user.is_looser:
        print('\nСОЖАЛЕЮ, но ВЫ ПРОИГРАЛИ... Нужно быть внимательнее!')
        break

    user.card.show()
    compic.card.show()

    user.stats()
    compic.stats()
    bag.stats()

    # game.check_winner(players)

    if user.is_winner and compic.is_winner:
        print('НИЧЬЯ!!!')
        break
    elif user.is_winner:
        print('ВЫ ПОБЕДИТЕЛЬ!')
        break
    elif compic.is_winner:
        print('КОМПИК ПОБЕДИТЕЛЬ!')
        break
    print('Игра продолжается...\n')



