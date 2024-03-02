def find_first(pred, iterable):
    for element in iterable:
        if pred(element):
            return element
    return None

def def_builder(names, constructor):
    clean_names = [name.split(".")[-1] for name in names]
    return [
        f"{constructor}('{clean_name}')"
        for name, clean_name in zip(names, clean_names)
    ]
