
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

def apply_tsne(df):
    X = np.array(df['Embeddings'].to_list(), dtype=np.float32)
    tsne = TSNE(random_state=0, n_iter=1000)
    tsne_results = tsne.fit_transform(X)
    df_tsne = pd.DataFrame(tsne_results, columns=['TSNE1', 'TSNE2'])
    df_tsne['Class Name'] = df['Class Name']
    return df_tsne

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
