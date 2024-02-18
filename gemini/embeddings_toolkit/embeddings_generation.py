def generate_embeddings(data, model, batch_size=32):
    embeddings = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        embeddings.extend(model.embed(batch))
    return embeddings