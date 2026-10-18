from lab_python_test.figures import Rectangle, Square, Circle, print_area


def main():
    for figure in (Rectangle(5, 4), Square(5), Circle(5)):
        print(type(figure).__name__)
        print_area(figure)


if __name__ == "__main__":
    main()
