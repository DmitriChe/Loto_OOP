from loto_classes import Game

if __name__ == '__main__':

    num_compics = int(input('Введите число компьютерных игроков: '))
    num_users = int(input('Введите число живых игроков: '))

    game = Game()
    game.run(num_compics, num_users)
