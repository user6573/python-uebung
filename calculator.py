def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Division durch Null nicht erlaubt")
    return a / b

def modulo(a, b):
    return a % b

def power(a, b):
    return a ** b

if __name__ == "__main__":
    print("5 + 3 =", add(5, 3))
    print("5 - 3 =", subtract(5, 3))
    print("5 * 3 =", multiply(5, 3))
    print("6 / 3 =", divide(6, 3))
    print("7 % 3 =", modulo(7, 3))
    print("2 ^ 8 =", power(2, 8))
