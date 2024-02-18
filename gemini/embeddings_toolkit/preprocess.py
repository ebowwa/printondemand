def preprocess_data(data, preprocessors):
    for preprocessor in preprocessors:
        data = preprocessor(data)
    return data