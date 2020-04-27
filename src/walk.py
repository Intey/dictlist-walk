import typing as t


def walk(
    walking_object: t.Union[t.Dict, t.List],
    step_function: t.Callable[[str, t.Any], t.Any],
    origin_path: str = "",
) -> None:
    """
    Функция прохода по структуре словаря или массива и
    применения ``step_function`` функции к каждому конечному
    значению. Неконечными значениями являются словари или
    списки (и их наследники).
    Проход выполняется "в глубину". Функция ``step_function``
    вызывается, когда текущее знаение не является списком
    или словарем. В параметры функции будут переданы:
    * текущий путь к текущему значению
    * текущее значение
    Результат функции никак не используется.

    Для примеров и как ключи преобразуются для списков -
    читайте ``test_walk.py``

    :param walking_object: словарь или список, по которому
        будет выполнен проход
    :param step_function: функция которая вызывается на
        каждом оконечном значении
    :param origin_path: уже пройденный путь или путь, с
        которого мы начинаем проходить. Основной смысл - для
        формирования пути при рекурсивном вызове этой
        функции
    :return: Нет результата.
    """
    items: t.Iterable = []
    list_index = False
    if isinstance(walking_object, dict):
        items = walking_object.items()
    elif isinstance(walking_object, list):
        items = enumerate(walking_object)
        list_index = True
    else:
        assert False, "walk can be applied to list or dict"
    current_path = origin_path
    for k, i in items:
        if list_index:
            key = f"[{k}]"
        else:
            key = str(k)
        if origin_path == "":
            current_path = str(key)
        else:
            current_path = f"{origin_path}.{key}"
        if type(i) in [dict, list]:
            walk(i, step_function, current_path)
        else:
            step_function(current_path, i)
