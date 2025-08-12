def apply_filter(field, op, value):
    if op == "gte":
        return field >= value
    elif op == "lte":
        return field <= value
    else:
        return field == value
