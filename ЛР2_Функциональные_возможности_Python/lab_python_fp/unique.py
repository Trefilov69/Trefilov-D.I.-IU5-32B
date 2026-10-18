class Unique:
    """Ленивый итератор, сохраняющий первый исходный элемент."""
    def __init__(self, items, **kwargs):
        self.items = iter(items)
        self.ignore_case = kwargs.get("ignore_case", False)
        self.seen = []

    def __iter__(self):
        return self

    def __next__(self):
        for item in self.items:
            key = item.casefold() if self.ignore_case and isinstance(item, str) else item
            if key not in self.seen:
                self.seen.append(key)
                return item
        raise StopIteration


if __name__ == "__main__":
    data = ["a", "A", "b", "B", "a", "A", "b", "B"]
    print(list(Unique(data)))
    print(list(Unique(iter(data), ignore_case=True)))
