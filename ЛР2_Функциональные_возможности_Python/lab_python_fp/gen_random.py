from random import randint


def gen_random(num_count, begin, end):
    if num_count < 0 or begin > end:
        raise ValueError("Количество неотрицательно; начало не больше конца")
    for _ in range(num_count):
        yield randint(begin, end)


if __name__ == "__main__":
    print(list(gen_random(5, 1, 3)))
