from functools import wraps


def print_result(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        print(func.__name__)
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"{key} = {value}")
        elif isinstance(result, list):
            for value in result:
                print(value)
        else:
            print(result)
        return result
    return wrapped


if __name__ == "__main__":
    @print_result
    def test_1():
        return 1

    @print_result
    def test_2():
        return "iu5"

    @print_result
    def test_3():
        return {"a": 1, "b": 2}

    @print_result
    def test_4():
        return [1, 2]

    for function in (test_1, test_2, test_3, test_4):
        function()
