from math import radians
import random
import time
import json
import os
from exceptions import NotCorrectColorIndex

DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DATA = f"{DIR}/data/"


class RedBlack:
    def __init__(self, user_color_index, bet):
        self.red_numbers = [number for number in range(1, 51)]
        self.black_numbers = [number for number in range(51, 101)]
        self.green_numbers = [0 for number in range(15)]
        self.game_box = self.red_numbers + self.black_numbers + self.green_numbers
        self.bet = bet
        self.user_number = self.__from_color_index_to_number(user_color_index)

    def start_game(self):
        self.__shuffle_game_box()
        self.game_number = self.__generate_number()

    def get_prize_color_bet(self):
        if (self.game_number in self.red_numbers and \
            self.user_number in self.red_numbers) or \
            (self.game_number in self.black_numbers and \
            self.user_number in self.black_numbers):
            return self.bet * 2
        elif self.game_number in self.green_numbers and \
            self.user_number in self.green_numbers:
            return self.bet * 14
        return 0

    def check_correct_index_color(function):
        def wrapper(self, user_color_index, *args, **kwargs):
            if user_color_index not in range(0, 3):
                raise NotCorrectColorIndex("Введите корректный индекс цвета")
            return function(self, user_color_index, *args, **kwargs)
        return wrapper

    def __shuffle_game_box(self):
        return random.shuffle(self.game_box)

    def __generate_number(self):
        return random.sample(self.game_box, 1)[0]

    @check_correct_index_color
    def __from_color_index_to_number(self, user_color_index):
        if user_color_index == 1:
            return random.sample(self.red_numbers, 1)[0]
        elif user_color_index == 2:
            return random.sample(self.black_numbers, 1)[0]
        return 0

class GameInteface:
    def __init__(self, game):
        self.game = game
    
    @staticmethod
    def writing_game_statistics():
        if os.path.isfile(PATH_DATA + "stat_game.json"):
            with open(PATH_DATA + "stat_game.json", "r", encoding="utf-8") \
                      as json_file:
                data = json.load(json_file)
        else:
            data = []
        data = data + [{"game_number": game.game_number}]
        with open(PATH_DATA + "stat_game.json", "w", encoding="utf-8") \
                  as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    @staticmethod
    def checking_correctness_of_bid():
        try:
            user_bet = int(user_bet_temp)
        except ValueError:
            print('Введите число')
            return 0
        if user_bet > 300:
            print('Максимаольная ставка 300')
            return 0
        elif user_bet > user.bank:
            print('У вас нет такой суммы')
            return 0
        return user_bet

    def drop_effect(function):
        def wrapper(self, *args, **kwargs):
            game_number_index = self.game.game_box.index(self.game.game_number)
            print_time = 20 + random.randint(0, 20)
            if game_number_index >= print_time:
                numbers = self.game.game_box[game_number_index - 20:game_number_index]
            else:
                numbers = self.game.game_box[game_number_index: game_number_index + 20]
            for index, number in enumerate(numbers, 1):
                print(f"{number}\n", end='')
                time.sleep(.1 + index/25)
            return function(self, *args, **kwargs)
        return wrapper

    @drop_effect
    def game_result_information(self):
        if self.game.game_number in self.game.red_numbers:
            print(f"Выпало красное -- {self.game.game_number}")
        elif self.game.game_number in self.game.black_numbers:
            print(f"Выпало чёрное -- {self.game.game_number}")
        else:
            print(f"Выпало зелёное -- {self.game.game_number}")

    def checking_winning(self):
        game_result = self.game.get_prize_color_bet()
        if game_result < 0:
            print("К сожанию, вы проиграли")
        else:
            print("Поздравялем с победой!")

class User:
    def __init__(self, user_hash):
        self.username = user_hash["username"]
        self.bank = user_hash["bank"]

    @staticmethod
    def writing_user_statistics():
        if os.path.isfile(PATH_DATA + "stat_user.json"):
            with open(PATH_DATA + "stat_user.json", "r", encoding="utf-8") \
                      as json_file:
                data = json.load(json_file)
        else:
            data = []
        if user_color_choice == 1:
            user_color_word = 'Крсное'
        elif user_color_choice == 2:
            user_color_word = 'Черное'
        else:
            user_color_word = 'Зеденое'
        data = data + [{"username": username, \
                       "user_bank": user.bank, \
                       "user_bet": user_bet, \
                       "user_color_word": user_color_word, \
                       "prize": prize}]
        with open(PATH_DATA + "stat_user.json", "w", encoding="utf-8") \
                  as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def print_bank(self):
        print(f"Ваш банк -- {self.bank}")

    def update_user_bank(self, bet):
        return self.bank + bet

print("Добро пожаловать в игру")
username = input("Введите ваш ник: ")
flag = True
while flag:
    try:
        user_bank = int(input("Ваш банк: "))
    except ValueError:
        print('Введите число')
        continue
    user = User({"username": username, "bank": user_bank})
    if user.bank <= 0:
        print("ваш банк не может быть отрицательным или нулевым")
        continue
    user_bet_temp = input("Введите вашу ставку: ")
    user_bet = GameInteface.checking_correctness_of_bid()
    if not user_bet:
        continue
    print("0. Зелёное\n1. Красное\n2. Чёрное")
    try:
        user_color_choice = int(input("Цвет (выберете цифрой): "))
    except ValueError:
        print('Введите число')
        continue
    user.bank -= user_bet
    game = RedBlack(user_color_choice, user_bet)
    game.start_game()
    prize = game.get_prize_color_bet()
    console = GameInteface(game)
    console.game_result_information()
    console.checking_winning()
    user.bank += prize
    print(f"Ваш банк -- {user.bank}")
    User.writing_user_statistics()
    GameInteface.writing_game_statistics()
    print('Хотите испытать удачу?\n1.Да,я рискну\n2.Нет,прервать игру')
    flag = input() == '1'

    