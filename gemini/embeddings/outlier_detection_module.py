
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_20newsgroups
from sklearn.manifold import TSNE
from tqdm.auto import tqdm
from google.api_core import retry
import google.generativeai as genai
import google.ai.generativelanguage as glm

# Function to configure API
def configure_api(api_key):
    genai.configure(api_key=api_key)

# Function to fetch and preprocess dataset
def fetch_and_preprocess_data():
    newsgroups_train = fetch_20newsgroups(subset='train')
    # Apply functions to remove names, emails, and extraneous words
    newsgroups_train.data = [re.sub(r'[\w\.-]+@[\w\.-]+', '', d) for d in newsgroups_train.data]
    newsgroups_train.data = [re.sub(r"\([^()]*\)", "", d) for d in newsgroups_train.data]
    newsgroups_train.data = [d.replace("From: ", "") for d in newsgroups_train.data]
    newsgroups_train.data = [d.replace("\nSubject: ", "") for d in newsgroups_train.data]
    # Cut off text entry after 5,000 characters
    newsgroups_train.data = [d[0:5000] if len(d) > 5000 else d for d in newsgroups_train.data]
    df_train = pd.DataFrame(newsgroups_train.data, columns=['Text'])
    df_train['Label'] = newsgroups_train.target
    # Match label to target name index
    df_train['Class Name'] = df_train['Label'].map(newsgroups_train.target_names.__getitem__)
    return df_train

# Function to sample and filter data
def sample_and_filter_data(df_train, sample_size=150, categories='sci'):
    df_train = (df_train.groupby('Label', as_index=False)
                .apply(lambda x: x.sample(sample_size))
                .reset_index(drop=True))
    if categories:
        df_train = df_train[df_train['Class Name'].str.contains(categories)]
    df_train = df_train.reset_index()
    return df_train

# Function to create embeddings
def create_embeddings(df, model='models/embedding-001'):
    tqdm.pandas()
    
    def make_embed_text_fn(model):
        @retry.Retry(timeout=300.0)
        def embed_fn(text: str) -> list[float]:
            embedding = genai.embed_content(model=model, content=text, task_type="clustering")['embedding']
            return np.array(embedding)
        return embed_fn
    
    df['Embeddings'] = df['Text'].progress_apply(make_embed_text_fn(model))
    df.drop('index', axis=1, inplace=True)
    return df

# Function for dimensionality reduction
def apply_tsne(df):
    X = np.array(df['Embeddings'].to_list(), dtype=np.float32)
    tsne = TSNE(random_state=0, n_iter=1000)
    tsne_results = tsne.fit_transform(X)
    df_tsne = pd.DataFrame(tsne_results, columns=['TSNE1', 'TSNE2'])
    df_tsne['Class Name'] = df['Class Name']
    return df_tsne

# Function for outlier detection
def detect_outliers(df, df_tsne, radius=0.62):
    def get_centroids(df_tsne):
        centroids = df_tsne.groupby('Class Name').mean()
        return centroids
    
    def calculate_euclidean_distance(p1, p2):
        return np.sqrt(np.sum(np.square(p1 - p2)))
    
    centroids = get_centroids(df_tsne)
    emb_centroids = {c: np.mean(df[df['Class Name'] == c]['Embeddings'], axis=0) for c in df['Class Name'].unique()}
    
    df['Outlier'] = False
    for idx, row in df.iterrows():
        dist = calculate_euclidean_distance(row['Embeddings'], emb_centroids[row['Class Name']])
        df.at[idx, 'Outlier'] = dist > radius
    
    outliers_projected = df_tsne.loc[df[df['Outlier']].index]
    return df, outliers_projected, centroids

# Function to visualize data and outliers
def visualize_data(df_tsne, outliers_projected, centroids):
    fig, ax = plt.subplots(figsize=(8,6))
    sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='Class Name', palette='Set2')
    sns.scatterplot(data=centroids, x='TSNE1', y='TSNE2', color="black", marker='X', s=100, label='Centroids')
    sns.scatterplot(data=outliers_projected, x='TSNE1', y='TSNE2', color='red', marker='o', alpha=0.5, s=90, label='Outliers')
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.title('Scatter plot with t-SNE and Outliers')
    plt.xlabel('TSNE1')
    plt.ylabel('TSNE2')
    plt.show()

# Main function to orchestrate the workflow
def main(api_key):
    configure_api(api_key)
    df_train = fetch_and_preprocess_data()
    df_train = sample_and_filter_data(df_train)
    df_train = create_embeddings(df_train)
    df_tsne = apply_tsne(df_train)
    df_train, outliers_projected, centroids = detect_outliers(df_train, df_tsne)
    visualize_data(df_tsne, outliers_projected, centroids)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        raise ValueError("API key is required as a command-line argument.")
    main(api_key)
