k = int(input('k='))
digits_count = 0
power_of_10 = 10
digits_in_square = 1
long_number = 0

i = 0

while digits_count < k:
    i += 1
    square = i ** 2
    if square >= power_of_10:
        power_of_10 *= 10
        digits_in_square += 1
    long_number = long_number * power_of_10 + square
    digits_count += digits_in_square

while digits_count > k:
    long_number //= 10
    digits_count -= 1

the_digit = long_number % 10
print('k-th digit', the_digit)

print('Digits in reversed order')
while long_number > 0:
    reversed_digit = long_number % 10
    long_number //= 10
    print(reversed_digit)
