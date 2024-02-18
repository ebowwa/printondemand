def filter_data(data, filter_function):
    return [item for item in data if filter_function(item)]