
import re
from sklearn.datasets import fetch_20newsgroups
import pandas as pd

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
