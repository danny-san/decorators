from datetime import datetime as dt
from random import randint

from access_control import access_control
from constants import ADMIN_USERNAME, UNKNOWN_COMMAND

start_time = dt.now()


class Game:
    def __init__(self):
        self.total_games = 0
        self.number = randint(1, 100)

    @access_control
    def get_statistics(self, *args, **kwargs) -> None:
        game_time = dt.now() - start_time
        print(f'Общее время игры: {game_time}, текущая игра - №{self.total_games}')

    @access_control
    def get_right_answer(self, *args, **kwargs) -> None:
        print(f'Правильный ответ: {self.number}')

    def check_number(self, username: str, guess: int) -> bool:
        # Если число угадано...
        if guess == self.number:
            print(f'Отличная интуиция, {username}! Вы угадали число :)')
            # ...возвращаем True
            return True

        if guess < self.number:
            print('Ваше число меньше того, что загадано.')
        else:
            print('Ваше число больше того, что загадано.')
        return False

    def game(self, username: str) -> None:
        print(
            '\nУгадайте число от 1 до 100.\n'
            'Для выхода из текущей игры введите команду "stop"'
        )
        while True:
            # Получаем пользовательский ввод,
            # отрезаем лишние пробелы и переводим в нижний регистр.
            user_input = input('Введите число или команду: ').strip().lower()

            match user_input:
                case 'stop':
                    break
                case 'stat':
                    self.get_statistics(username=username)
                case 'answer':
                    self.get_right_answer(username=username)
                case _:
                    try:
                        guess = int(user_input)
                    except ValueError:
                        print(UNKNOWN_COMMAND)
                        continue

                    if self.check_number(username, guess):
                        break


def get_username() -> str:
    username = input('Представьтесь, пожалуйста, как Вас зовут?\n').strip()
    if username == ADMIN_USERNAME:
        print(
            '\nДобро пожаловать, создатель! '
            'Во время игры вам доступны команды "stat", "answer"'
        )
    else:
        print(f'\n{username}, добро пожаловать в игру!')
    return username


def guess_number() -> None:
    username = get_username()
    # Счётчик игр в текущей сессии.
    round = Game()
    while True:
        round.total_games += 1
        round.game(username)
        play_again = input('\nХотите сыграть ещё? (yes/no) ')
        if play_again.strip().lower() not in ('y', 'yes'):
            break


if __name__ == '__main__':
    print(
        'Вас приветствует игра "Угадай число"!\n'
        'Для выхода нажмите Ctrl+C'
    )
    guess_number()
