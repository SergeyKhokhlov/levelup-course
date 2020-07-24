a, b, c = str(input())
a = int(a)
b = int(b)
c = int(c)
if a % 2 == 0 and b % 2 == 0 and c % 2 != 0 or a % 2 == 0 and c % 2 == 0 and b % 2 != 0 \
        or c % 2 == 0 and b % 2 == 0 and a % 2 != 0:
    if a != b and b != c and a != c:
        print("Пароль установлен!")
    else:
        print("Цифры в пароле повторяются!")
else:
    print("В пароле должна быть 1 нечётная и 2 чётные цифры!")