from cs50 import get_int
import re


def luhn_algo(num):
    """Fetches Luhn's Algorithm sum, which is the sum of each products' digit
    starting with the second-to-last digit multiplied by 2, then sum that with
    the digits that were not multiplied by 2.

    Args:
        num: An integer (i.e., 4003600000000014)

    Returns:
        Sum of each individual products digit starting with the second-to-last digit
        multiplied by 2. Then add that sum to the sum of the digits that were not
        multiplied by 2.

        Example: calling function on 4003600000000014 would return 20
    """
    sum = 0
    num_string = str(num)   # Converts num into string type
    # Starts with second to last digit
    # iterates by -2 until length of string is reached
    for i in range(-2, -len(num_string) - 1, -2):
        dig_product = int(num_string[i]) * 2
        if dig_product > 9:     # If product is 2 digits, sum both individual digits
            sum += dig_product % 10
            sum += dig_product // 10  # int division to get first digit
        else:
            sum += dig_product % 10
    for i in range(-1, -len(num_string) - 1, -2):
        sum += int(num_string[i])
    return sum


def is_valid(luhn_sum):
    # Checks if last digit of Luhn's Algorith sum is 0
    return luhn_sum % 10 == 0


def creditor(credit_num):
    """Prints out the creditor of the credit card number (VISA, MASTERCARD, AMEX)
    VISA: 13 or 16 digit numbers; begins with 4.
    MASTERCARD: 16 digit numbers; begins with 51, 52, 53, 54, or 55
    AMEX: 15 digit numbers; begins with 34 or 37
    INVALID: credit number does not match any of the above criterias

    Args:
        credit_num: An integer representing a credit card number (i.e., 4003600000000014)

    Returns:
        None - prints out one of the following:

        'VISA', 'MASTERCARD', 'AMEX', or 'INVALID'
        Example: 4003600000000014 would print VISA
    """
    str_credit = str(credit_num)

    # Checks if card is Visa, Mastercard, Amex, or neither
    if (len(str_credit) == 13 or len(str_credit) == 16) and bool(re.search("^4", str_credit)):
        print('VISA')
    elif (len(str_credit) == 16 and (bool(re.search("^51", str_credit)) or bool(re.search("^52", str_credit)) or bool(re.search("^53", str_credit)) or bool(re.search("^54", str_credit)) or bool(re.search("^55", str_credit)))):
        print('MASTERCARD')
    elif (len(str_credit) == 15 and (bool(re.search("^34", str_credit)) or bool(re.search("^37", str_credit)))):
        print('AMEX')
    else:
        print('INVALID')


def main():
    while True:
        credit_num = get_int('Number: ')
        if credit_num > 0:
            break

    luhn_sum = luhn_algo(credit_num)
    if is_valid(luhn_sum):
        creditor(credit_num)
    else:
        print('INVALID')


if __name__ == "__main__":
    main()

