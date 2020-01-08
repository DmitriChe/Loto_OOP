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

