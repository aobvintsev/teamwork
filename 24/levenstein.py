# відстань Левенштейна

def levenstein(s1, s2):
    if not s1 and not s2:
        d = 0
    elif not s1:
        d = len(s2)
    elif not s2:
        d = len(s1)
    else:
        cost = 0 if s1[-1] == s2[-1] else 1
        d = min(levenstein(s1[:-1], s2[:-1]) + cost,
                levenstein(s1[:-1], s2) + 1,
                levenstein(s1, s2[:-1]) + 1)
    return d

s1 = input('s1= ')
s2 = input('s2= ')
d = levenstein(s1, s2)
print('d=', d)
