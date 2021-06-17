import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS card (
id INTEGER PRIMARY KEY,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0);''')
cur.execute('DELETE FROM card;')
conn.commit()

user_main_input = ''
user_logged_input = ''
logged_in = False
logged_card = ''


def main_menu():
    global user_main_input
    print('''1. Create an account
2. Log into account
0. Exit''')
    user_main_input = input()


def logged_in_menu():
    global user_logged_input
    print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
    user_logged_input = input()


def check_luhn(card):
    luhn_list = list(card)
    for i_1 in range(16):
        luhn_list[i_1] = int(luhn_list[i_1])
    for i_2 in range(8):
        luhn_list[2 * i_2] *= 2
        if luhn_list[2 * i_2] > 9:
            luhn_list[2 * i_2] -= 9
    addition = sum(luhn_list)
    if addition % 10 == 0:
        return True
    else:
        return False


def create_account():
    card_number = "400000" + str(random.randint(000000000, 999999999))
    card_list = list(card_number)
    for i_1 in range(15):
        card_list[i_1] = int(card_list[i_1])
    for i_2 in range(8):
        card_list[2 * i_2] *= 2
        if card_list[2 * i_2] > 9:
            card_list[2 * i_2] -= 9
    addition = sum(card_list)
    if addition % 10 == 0:
        card_number += '0'
    else:
        card_number += str(10 - addition % 10)

    card_pin = str(random.randint(0, 9)) + str(random.randint(0, 9)) \
               + str(random.randint(0, 9)) + str(random.randint(0, 9))

    cur.execute(f'INSERT INTO card (number, pin) VALUES ({card_number}, {card_pin});')
    conn.commit()
    print(f'''Your card has been created
Your card number:
{card_number}
Your card PIN:
{card_pin}''')


def log_into_account():
    global logged_in
    global logged_card

    cur.execute('SELECT number, pin FROM card;')
    accounts = cur.fetchall()

    print('Enter your card number:')
    card_input = input()
    print('Enter your PIN:')
    pin_input = input()
    if (card_input, pin_input) in accounts:
        print('You have successfully logged in!')
        logged_in = True
        logged_card = card_input
    else:
        print('Wrong card number or PIN!')


def exit_message():
    print('Bye!')


def get_balance():
    cur.execute(f'SELECT balance FROM card WHERE number = {logged_card};')
    balance = cur.fetchone()[0]
    print(f'Balance: {balance}')


def add_income():
    print('Enter income:')
    income = int(input())
    cur.execute(f'UPDATE card SET balance = balance + {income} WHERE number = {logged_card};')
    conn.commit()
    print('Income was added!')


def do_transfer():
    print('Transfer')
    print('Enter card number:')
    transfer_card = input()

    cur.execute(f'SELECT number FROM card;')
    existing_cards = cur.fetchall()

    if not check_luhn(transfer_card):
        print('Probably you made a mistake in the card number. Please try again!')
    else:
        if (transfer_card,) not in existing_cards:
            print('Such a card does not exist.')
        elif transfer_card == logged_card:
            print("You can't transfer money to the same account!")
        else:
            print('Enter how much money you want to transfer:')
            transfer = int(input())
            cur.execute(f'SELECT balance FROM card WHERE number = {logged_card};')
            available_balance = cur.fetchone()[0]
            if transfer > available_balance:
                print('Not enough money!')
            else:
                cur.execute(f'UPDATE card SET balance = balance + {transfer} WHERE number = {transfer_card};')
                cur.execute(f'UPDATE card SET balance = balance - {transfer} WHERE number = {logged_card};')
                conn.commit()


def close_account():
    cur.execute(f'DELETE FROM card WHERE number = {logged_card}')
    conn.commit()
    print('The account has been closed!')


while True:
    if not logged_in:
        main_menu()
        if user_main_input == '1':
            create_account()
        elif user_main_input == '2':
            log_into_account()
        elif user_main_input == '0':
            exit_message()
            break
    elif logged_in:
        logged_in_menu()
        if user_logged_input == '1':
            get_balance()
        elif user_logged_input == '2':
            add_income()
        elif user_logged_input == '3':
            do_transfer()
        elif user_logged_input == '4':
            close_account()
        elif user_logged_input == '5':
            logged_in = False
        elif user_logged_input == '0':
            exit_message()
            break
