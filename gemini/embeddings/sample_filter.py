
import pandas as pd

def sample_and_filter_data(df_train, sample_size=150, categories='sci'):
    df_train = (df_train.groupby('Label', as_index=False)
                .apply(lambda x: x.sample(sample_size))
                .reset_index(drop=True))
    if categories:
        df_train = df_train[df_train['Class Name'].str.contains(categories)]
    df_train = df_train.reset_index()
    return df_train
