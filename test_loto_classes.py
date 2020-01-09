# Инструкция по созданию тестов pytest: https://www.jetbrains.com/help/pycharm/pytest.html
from loto_classes import Bag, Card, Computer, User, Game
import unittest


class TestBag:

    def test_bag_init(self):
        bag = Bag()
        assert min(bag.nums) > 0
        assert max(bag.nums) < 91
        assert len(bag.nums) == 90

    def test_bag_next(self):
        bag = Bag()
        assert bag.nums[-1] == bag.next()

    def test_bag_str(self):
        bag = Bag()
        assert str(bag) != ''
        assert str(bag) == 'Всего 90 бочонков №№: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,' \
                           ' 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,' \
                           ' 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,' \
                           ' 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69,' \
                           ' 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, '

    def test_bag_eq(self):
        bag_one = Bag()
        bag_two = Bag()
        bag_three = Bag()
        bag_three.nums[0] = 100
        assert bag_one == bag_two
        assert bag_one != bag_three

    def test_bag_item(self):
        bag = Bag()
        bag.nums = sorted(bag.nums)
        assert bag.nums[0] == 1
        assert bag.nums[89] == 90
        assert bag.nums[44] == bag.nums[89] // 2
        assert bag.nums[0] != 0
        assert bag.nums[89] != 89

    def test_bag_len(self):
        bag = Bag()
        assert len(bag) == 90
        assert len(bag) == len(bag.nums)


class TestCard:

    def test_card_init(self):
        card = Card('Ivan')

        assert card.player_name == 'Ivan'

        assert min(card.card_nums) > 0
        assert max(card.card_nums) < 91
        assert len(card.card_nums) == 15

        assert min(card.place_idx) >= 0
        assert max(card.place_idx) < 27
        assert len(card.place_idx) == 15

        assert len(card.card.items()) == 27

    def test_card_modify(self):
        card = Card('Ivan')
        # card.card_nums  # [45, 32, 17, 81, ... , 13]
        # card.place_idx  # [3, 1, 4, 2, ... , 12]
        # card.card  # {3: 45, 1: 32, 4: 17, 2: 81, ... , 12: 13}

        assert card.card[card.place_idx[0]] == card.card_nums[0]

        card.modify(card.card_nums[0])
        assert card.card[card.place_idx[0]] is None


class TestComputer:

    def test_computer_name(self):
        computer = Computer()
        assert computer.name == 'Computer'
        computer = Computer('Mike')
        assert computer.name == 'Mike'
        del computer

    def test_computer_card(self):
        computer = Computer()
        assert computer.card.player_name == 'Computer'
        del computer

    def test_computer_nums(self):
        computer = Computer()
        assert computer.nums == computer.card.card_nums
        del computer

    def test_computer_iswinner(self):
        computer = Computer()
        assert computer.is_winner is False
        del computer

    def test_computer_step(self):
        computer = Computer()
        num = computer.nums[0]
        assert num in computer.nums
        computer.step(num)
        assert num not in computer.nums
        del computer

    def test_computer_stats(self):
        computer = Computer()
        assert bool(computer.name) is True
        assert type(computer.name) is str
        assert len(computer.nums) >= 0
        assert type(computer.nums) is list
        assert type(computer.nums[0]) is int
        del computer


class TestUser:

    def test_user_init(self):
        user = User()
        assert user.name == 'User'
        user = User('Ivan')
        assert user.name == 'Ivan'
        assert user.is_looser is False
        assert user.answers[0] == 'y'
        assert user.answers[1] == 'n'
        assert len(user.answers) == 2
        del user

    # def test_user_step(self):
    #     user = User()
    #     unreal_num = 99
    #     user.step(unreal_num)
    #     assert user.is_looser is True


class TestGame:

    def test_game_init(self):
        game = Game()
        assert game.num_users == 0
        assert game.num_compics == 0
        assert game.players == {}
        assert isinstance(game.bag, Bag)
        assert len(game.bag.nums) == 90
        assert game.winners == game.losers

    def test_game_generate_players(self):
        game = Game()
        game.generate_players(1, 1)
        assert len(game.players) == 2
        assert 'compic-1' in game.players.keys()
        assert 'user-1' in game.players.keys()
        assert 'compic-2' not in game.players.keys()
        assert 'user-2' not in game.players.keys()
        assert isinstance(game.players['compic-1'], Computer)
        assert isinstance(game.players['user-1'], User)
        game.generate_players(2, 2)
        assert len(game.players) == 4

    def test_game_check_winner(self):
        game = Game()
        assert game.check_winner() is False
        assert len(game.winners) == 0
        user = User()
        game.winners.append(user)
        user.is_winner = True
        assert game.check_winner() is True

