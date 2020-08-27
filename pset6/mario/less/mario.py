from cs50 import get_int

height = 0
while height < 1 or height > 8:
    height = get_int('Height: ')

for row in range(height):
    num_space = height - row - 1
    num_hash = row + 1
    print(' ' * num_space, end='')
    print('#' * num_hash)
