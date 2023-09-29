# Name: Zachary Zawodny
# Date: March 24th 2022
# Project 1: Point-Of-Sale System
# Version 3

import pps_emu
from time import sleep
import csv

products = []


# Adds the dictionaries to a list
def AddDict(row):
    global products
    add_dict = {'Item ID': int(row[0]), 'Item name': row[1], 'Price': float(row[2]), 'Amount': int(row[3])}
    products.append(add_dict)


# The function to print the receipt to a txt file
def PrintReceipt(total_cost):
    try:  # Try to write to the txt file with the users order data
        with open('receipt.txt', 'w') as writer:
            for i in products:  # start a for loop to display the grand total
                if i['Amount'] != 0:  # Checks if product has been ordered, if not we don't display it
                    writer.writelines('Item: {}\tDescription: {:<20}\tAmount: {} '  # Displays the menu, quantity and 
                                      # cost of your order 
                                      '\tPrice: $ {:>6.2f} \tItem Total: $ {:>6.2f}\n'.format(i['Item ID'],
                                                                                              i['Item name'],
                                                                                              i['Amount'],
                                                                                              i['Price'],
                                                                                              i['Amount'] *
                                                                                              i['Price']))
            writer.writelines("\nToday's Total is: ${:>6.2f}".format(total_cost))
    except FileNotFoundError:  # FileNotFoundError catching is not avail on Trinket
        print()
        print('File couldn\'t be created, exiting program...')  # Issue a message
        exit()  # Exit the program early


# The function to display the receipt to the console
def DisplayReceipt(total_cost):
    for i in products:  # start a for loop to display the grand total
        if i['Amount'] != 0:  # Checks if product has been ordered, if not we don't display it
            print('Item: {}\tDescription: {:<20}\tAmount: {} '  # Displays the menu, quantity and cost of your order
                  '\tPrice: $ {:>6.2f} \tItem Total: $ {:>6.2f}'.format(i['Item ID'],
                                                                        i['Item name'],
                                                                        i['Amount'],
                                                                        i['Price'],
                                                                        i['Amount'] *
                                                                        i['Price']))
    print("Today's total is:                                                                 "
          "\t \t$ {:>6.2f}".format(total_cost))  # Prints the total cost


def main():
    global products
    sensor = pps_emu.Sensor()  # Reference to the pps emu sensor

    try:  # Try to open the csv file with the menu data
        with open('products.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                AddDict(row)
    except FileNotFoundError:  # FileNotFoundError catching is not avail on Trinket
        print()
        print('File couldn\'t be created, exiting program...')  # Issue a message
        exit()  # Exit the program early

    print("   Welcome to Zach's Beach side restaurant.\n"  # Welcoming Text
          'We have the following Items that you can order:')

    for i in products:  # A for loop to Display all the menu items and their prices
        print('Item {:>1}: {:<20}\tPrice: ${:>4.2f}'.format(i['Item ID'], i['Item name'], i['Price']))

    while True:  # Loop that holds the ordering logic
        order_input = input("Input a valid item id to order,"
                            ' and type "done" to submit your order: ')  # Asks user what item they want
        if order_input == 'done':  # Checks if the user is done ordering
            break  # leaves the while loop
        if int(order_input) > len(products) or int(order_input) <= 0:  # Checks if the order isn't a valid Item ID
            print('Please input a valid Item ID')
        else:  # Anything else would be a valid item ID
            order_amount = input("Please input the quantity you would like: ")  # Asks user how much they want
            if int(order_amount) < 0:  # Checks if the order amount isn't a valid quantity
                print('Please input a valid Item quantity')
            else:  # anything else would be a valid quantity
                products[int(order_input) - 1]['Amount'] = int(order_amount)  # Change Amount key to the order amount

    total_cost = 0.0  # Creating a float variable to store the total cost of the order
    for i in products:
        total_cost = i['Amount'] * i['Price'] + total_cost  # keeps track of the total cost
    if total_cost == 0:  # Checks if the cost is nothing, if so we give them an exit response
        print('If you wish to order anything please restart the program, otherwise, have a great day!')
        exit()

    while True:  # A while loop to get the users desired output
        option_input = input(
            'If you desire a a receipt save to a file, type "f". If you want the receipt displayed to the'
            'console, type "c". If you would like both, type "b"')

        if option_input == 'f' or option_input == 'c' or option_input == 'b':
            if option_input == 'f':
                print("Thank you for shopping at Zach's Beach side restaurant")
                PrintReceipt(total_cost)
                break
            if option_input == 'c':
                print("Thank you for shopping at Zach's Beach side restaurant")
                DisplayReceipt(total_cost)
                break
            if option_input == 'b':
                print("Thank you for shopping at Zach's Beach side restaurant")
                PrintReceipt(total_cost)
                DisplayReceipt(total_cost)
                break
        else:  # if not a valid option, tell the user such
            print('Please input a valid option')

    for i in range(0, 15):  # Starts a for loop that runs 15 times exactly, Used to flash the
        # light and alert kitchen
        sensor.output('rled', 'on')  # Turns on Red Led
        sleep(0.5)  # Waits a half of a second
        sensor.output('rled', 'off')  # Turns off Red Led
        sleep(0.5)  # Waits a half of a second


if __name__ == '__main__':
    main()
