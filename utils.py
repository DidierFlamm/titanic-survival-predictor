import streamlit as st
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"


def set_seed():
    if "seed" not in st.session_state:
        st.session_state.seed = random.randint(0, 2**32 - 1)
    seed = st.session_state.seed
    random.seed(seed)
    np.random.seed(seed)


@st.cache_data
def load_csv():
    df = pd.read_csv(url, index_col="PassengerId")
    df.index.name = "#"
    return df


@st.cache_data
def preprocess_data(df: pd.DataFrame, split: bool):
    # features
    X = df.copy()

    X = X.drop(
        ["Name", "Ticket", "Cabin"],
        axis=1,
    )

    # feature engineering
    X["Family"] = X["SibSp"] + X["Parch"] + 1
    X["IsAlone"] = (X["Family"] == 1).astype(int)

    # target
    y = X.pop("Survived")

    # Train/test split
    if split:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y
        )
    else:
        X_train, X_test, y_train, y_test = X, None, y, None

    # gestion des valeurs manquantes (age : médiane, embarked : mode)
    age_median = X_train["Age"].median()
    embarked_mode = X_train["Embarked"].mode()[0]

    X_train["Age"] = X_train["Age"].fillna(age_median)
    X_train["Embarked"] = X_train["Embarked"].fillna(embarked_mode)

    if X_test is not None:
        X_test["Age"] = X_test["Age"].fillna(age_median)
        X_test["Embarked"] = X_test["Embarked"].fillna(embarked_mode)

    # scaling des variables numériques
    num_cols = ["Age", "Fare", "SibSp", "Parch", "Pclass", "Family"]
    scaler = StandardScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])

    if X_test is not None:
        X_test[num_cols] = scaler.transform(X_test[num_cols])

    # encodage des variables catégorielles
    categorical_cols = ["Sex", "Embarked"]
    X_train = pd.get_dummies(X_train, columns=categorical_cols, drop_first=True)

    if X_test is not None:
        X_test = pd.get_dummies(X_test, columns=categorical_cols, drop_first=True)
        # Réindexation pour garantir le même ordre des colonnes (pas garanti apres oh encodage)
        X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    return X_train, X_test, y_train, y_test
