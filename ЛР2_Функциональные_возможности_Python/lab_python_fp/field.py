def field(items, *args):
    """Выдать непустые значения или проекции словарей на заданные поля."""
    assert args, "Необходимо указать хотя бы одно поле"
    for item in items:
        if len(args) == 1:
            value = item.get(args[0])
            if value is not None:
                yield value
        else:
            result = {key: item[key] for key in args if item.get(key) is not None}
            if result:
                yield result


if __name__ == "__main__":
    goods = [{"title": "Ковер", "price": 2000, "color": "green"},
             {"title": "Диван для отдыха", "color": "black"}]
    print(list(field(goods, "title")))
    print(list(field(goods, "title", "price")))
