import math


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n) + 1), 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def next_prime(n):
    if n <= 1:
        return 2
    prime = int(n)
    found = False
    while not found:
        prime += 1
        if is_prime(prime):
            found = True
    return prime


def hash_value(table, key):
    h = hash(key)
    a = table["scale"]
    b = table["shift"]
    p = table["prime"]
    m = table["capacity"]
    value = int((abs(a * h + b) % p) % m)
    return value
