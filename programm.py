from math import radians
import random
import time
import json
import os
import inspect
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
        self.userpassword = user_hash["userpassword"]
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

    @staticmethod
    def load_users():
        users = []
        if os.path.isfile(PATH_DATA + "users.json"):
            with open(PATH_DATA + "users.json", "r", encoding="utf-8") \
                      as read_file:
                data = json.load(read_file)
            for user_hash in data:
                users.append(user_hash)
        return users

    @check_correct_password
    @check_correct_username
    @staticmethod
    def user_registration(username, userpassword, users):
        for user in users:
            if user['username'] == username:
                return 'Такой пользователь уже зарегистрирован'
        users.append({"username": username, \
                      "userpassword": userpassword})
        with open(PATH_DATA + "users.json", "w", encoding="utf-8") \
                  as json_file:
            json.dump(users, json_file, ensure_ascii=False, indent=4)
        return 'Пользователь успешно добавлен'

    def check_correct_password(function):
        def wrapper(self, userpassword, *args, **kwargs):
            if len(userpassword) < 8:
                raise NotCorrectColorIndex("Минимальнвя длина пароля \
                                           8 символов")
            return function(self, userpassword, *args, **kwargs)
        return wrapper

    def check_correct_username(function):
        def wrapper(self, username, *args, **kwargs):
            if not username.startswith('@'):
                raise NotCorrectColorIndex("Ник должен начинаться с @")
            flag = False  # В пароле нет цифр
            for i in username:
                if i in '0123456789':
                    flag = True
                    break
            if flag:
                raise NotCorrectColorIndex("Ник не должен \
                                           содержать цифр")
            return function(self, username, *args, **kwargs)
        return wrapper

    def user_authorization(username, userpassword, users):
        for user in users:
            if user['username'] == username and \
               user['userpassword'] == userpassword:
                return True
        return False

    def print_bank(self):
        print(f"Ваш банк -- {self.bank}")

    def update_user_bank(self, bet):
        return self.bank + bet

    def add_bonus(function):
        def wrapper(self, add_bank, *args, **kwargs):
            if add_bank > 1000:
                add_bank +=100
            return function(self, add_bank, *args, **kwargs)
        return wrapper

    @add_bonus
    def adding_money_to_bank(self, add_bank):
        return self.bank + add_bank

print("Добро пожаловать в игру")
flag = True
while flag:
    print(inspect.cleandoc('''Что желаете (введите номер пункта):
                           1. Зарегистрироваться
                           2. Авторизироваться
                           3. Выйти из программы
                           '''))
    user_choice = input()
    if user_choice == '1':  # Регистрация
        username = input("Введите ваш ник: ")
        userpassword = input('Введите ваш пароль: ')
        users = User.load_users()
        print(User.user_registration(username, userpassword, users))
        continue
    elif user_choice == '2':  # Авторизация
        username = input("Введите ваш ник: ")
        userpassword = input('Введите ваш пароль: ')
        users = User.load_users()
        if not User.user_authorization(username, userpassword, users):
            print('Ошибка в имени или пароле пользователя')
            continue
    elif user_choice == '3':  # Выход из программы
        flag = False
        continue
    else:
        print('Такого варианта не предусмотррено')
        continue
    try:
        user_bank = int(input("Ваш банк: "))
    except ValueError:
        print('Введите число')
        continue
    user = User({"username": username, "userpassword": userpassword, 
                 "bank": user_bank})
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
    print('Хотите добавить денег в банк?\n1.Да\n2.Нет')
    if input() == '1':
        try:
            add_bank = int(input('Введите сумму: '))
        except ValueError:
            print('Введите число')
            continue
        user.bank = user.adding_money_to_bank(add_bank)
        user.print_bank()

