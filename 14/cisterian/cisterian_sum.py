from cisterian import CisterianNumber, SCALE_X, SCALE_Y

numbers = list(map(int, input('numbers? ').split()))
s = CisterianNumber(0)
start_x = x = -200
y = 200
for i in numbers:
    c = CisterianNumber(i)
    c.show(x, y)
    s = s.add(c)
    x += SCALE_X + SCALE_X // 2
y -= (SCALE_Y + SCALE_Y // 2)
s.show(start_x, y)
k = input()
