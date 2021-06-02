import random
import re

MajorIndIdent = 4,
BankIdNum = *MajorIndIdent, 0, 0, 0, 0, 0
name_file = 'existing_bank_cards.txt'


class Card:
    def __init__(self, number, pin, money):
        self.__number = number
        self.__pin = pin
        self.__money = money

    def is_valid(self):
        if type(self.__number != str or type(self.__pin != str or type(self.__money != str))):
            return False
        num = tuple(tuple(int(x) for x in self.__number))
        num = tuple((num[i] if i % 2 != 0 else num[i] * 2) for i in range(len(num)))
        num = tuple((num[i] // 10 + num[i] % 10 if num[i] > 9 else num[i]) for i in range(len(num)))
        return sum(num) % 10 == 0

    def save(self, function):
        f = open(name_file, "a")
        f.write('\nnum_card - ' + self.__number + '\npin - ' + self.__pin + '\nmoney - ' + self.__money)
        f.close()
        function(self.__number, self.__pin)

    def login(self, pin):
        return self.__pin == pin

    def get_money(self, pin):
        return self.__money if self.__pin == pin else None

    @property
    def number(self):
        return self.__number


def get_number_new_card():
    while True:
        num = tuple((*BankIdNum, *tuple(random.randint(0, 9) for _ in range(9))))
        num2 = num[:]
        num2 = tuple((num2[i] if i % 2 != 0 else num2[i] * 2) for i in range(len(num)))
        num2 = tuple((num2[i] // 10 + num2[i] % 10 if num2[i] > 9 else num2[i]) for i in range(len(num2)))
        num = *num, 0 if sum(num2) % 10 == 0 else (10 - sum(num2) % 10)
        number_new_card = ''.join(list(str(number) for number in num))
        if number_new_card not in get_numbers_existing_cards():
            break
    return number_new_card


def get_new_pin():
    return ''.join((str(random.randint(0, 9)) for i in range(4)))


def get_all_cards():
    regex = r"num_card\s?-\s?(\d{16})\npin\s?-\s?(\d{4})\nmoney\s?-\s?(\d+.?\d*)"
    try:
        f = open(name_file)
    except FileNotFoundError:
        return ''

    matches = re.finditer(regex, f.read(), re.MULTILINE)
    f.close()
    return list(Card(group[0], group[1], group[2]) for group in list(match.groups() for match in matches))


def get_numbers_existing_cards():
    cards = get_all_cards()
    return list(card.number for card in cards)


def create_new_card(function):
    card = Card(get_number_new_card(), get_new_pin(), '0')
    card.save(function)
    return card


def test():
    while True:
        choise = input('1. Create an account\n2. Log into account\n0. Exit\n >> ')
        if choise == '0':
            print('Bye!')
            break
        elif choise == '1':
            card = create_new_card((lambda num, pin: print(
                'Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}'.format(num, pin))))
        elif choise == '2':
            number_card = input('Enter your card number:\n >> ')
            pin = input('Enter your PIN:\n >> ')

            try:
                card = list(card for card in get_all_cards() if card.number == number_card and card.login(pin))[0]
            except IndexError:
                print('Wrong card number or PIN!')
                continue
            else:
                print('You have successfully logged in!')
                check = True
                while check:
                    choise = input('1. Balance\n2. Log out\n0. Exit\n >> ')
                    if choise == '0':
                        break
                    elif choise == '1':
                        print('Balance ', card.get_money(pin))
                    elif choise == '2':
                        print('You have successfully logged out!')
                        check = False
                    else:
                        print('Not correct enter.')
                else:
                    continue
                break
        else:
            print("Not correct enter.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
