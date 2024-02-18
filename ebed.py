from gemini.embeddings.preprocess import fetch_and_preprocess_data
from gemini.embeddings.sample_filter import sample_and_filter_data
from gemini.embeddings.embeddings import create_embeddings
from gemini.embeddings.tsne_visualization import apply_tsne, visualize_data
from gemini.auth_gemini import get_api_key

def main():
    # Fetch and preprocess data
    df_train = fetch_and_preprocess_data()

    # Sample and filter data
    df_train = sample_and_filter_data(df_train)

    # Create embeddings
    df_train = create_embeddings(df_train)

    # Apply t-SNE and visualize
    df_tsne = apply_tsne(df_train)
    df_train, outliers_projected, centroids = detect_outliers(df_train, df_tsne)
    visualize_data(df_tsne, outliers_projected, centroids)

if __name__ == "__main__":
    main()