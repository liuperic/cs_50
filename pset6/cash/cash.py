from cs50 import get_float
from math import floor

while True:
    change = get_float('Change owed: ')
    if change >= 0:
        break

cents = floor(change * 100)

quarters = cents // 25
dimes = (cents % 25) // 10
nickels = (cents % 25 % 10) // 5
pennies = cents % 25 % 10 % 5

print(quarters + dimes + nickels + pennies)
