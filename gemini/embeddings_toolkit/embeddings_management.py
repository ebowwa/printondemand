import pickle

def save_embeddings(embeddings, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(embeddings, f)

def load_embeddings(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)