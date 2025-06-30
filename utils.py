import streamlit as st
from google.cloud import translate_v2 as translate
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


csv_url = (
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

translate_client = translate.Client()


@st.cache_data
def translate_text(text, language):
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        return translate_client.translate(text, target_language=language)[
            "translatedText"
        ]
    else:
        return text


def set_seed():
    if "seed" not in st.session_state:
        st.session_state.seed = random.randint(0, 2**32 - 1)
    seed = st.session_state.seed
    random.seed(seed)
    np.random.seed(seed)


@st.cache_data
def load_csv(drop_outliers: bool):
    df = pd.read_csv(csv_url, index_col="PassengerId")
    df.index.name = "#"
    if drop_outliers:
        df = df[df.Fare < 500]
    return df


@st.cache_data
def get_fare_bounds(df):
    """returns a dict with min, median and max fare from each class"""
    return {
        1: {
            "min": df[df.Pclass == 1]["Fare"].min(),
            "median": df[df.Pclass == 1]["Fare"].median(),
            "max": df[df.Pclass == 1]["Fare"].max(),
        },
        2: {
            "min": df[df.Pclass == 2]["Fare"].min(),
            "median": df[df.Pclass == 2]["Fare"].median(),
            "max": df[df.Pclass == 2]["Fare"].max(),
        },
        3: {
            "min": df[df.Pclass == 3]["Fare"].min(),
            "median": df[df.Pclass == 3]["Fare"].median(),
            "max": df[df.Pclass == 3]["Fare"].max(),
        },
    }


@st.cache_data
def preprocess_data(
    df: pd.DataFrame, split: bool
) -> tuple[pd.DataFrame, pd.DataFrame | None, pd.Series | None, pd.Series | None]:
    # features
    X = df.copy()

    # drop outliers
    X = X[X["Fare"] < 500]

    # drop "Name", "Ticket" and Cabin except for custom passenger who doesn't have
    cols_to_drop = set(["Name", "Ticket", "Cabin"]).intersection(X.columns)
    X = X.drop(list(cols_to_drop), axis=1)

    # feature engineering
    X["Family"] = X["SibSp"] + X["Parch"] + 1
    X["IsAlone"] = (X["Family"] == 1).astype(int)

    # target
    if "Survived" in X.columns:
        y = X.pop("Survived")
    else:  # custom passenger doesn't have "survived"
        y = None

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

    # memorize le scaler
    if "scaler" not in st.session_state:
        scaler = StandardScaler()
        X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
        st.session_state.scaler = scaler
    else:
        X_train[num_cols] = st.session_state.scaler.transform(X_train[num_cols])

    if X_test is not None:
        X_test[num_cols] = st.session_state.scaler.transform(X_test[num_cols])

    # encodage des variables catégorielles
    categorical_cols = ["Sex", "Embarked"]
    X_train = pd.get_dummies(X_train, columns=categorical_cols, drop_first=False)

    # memorize les colonnes pour pouvoir réindexer le X custom qui n'aura pas toutes les colones OH
    if "columns" not in st.session_state:
        st.session_state.columns = X_train.columns
    else:
        X_train = X_train.reindex(columns=st.session_state.columns, fill_value=0)

    # on a choisi drop_first = False car sinon les colonnes OH de la prediction du custom sont droped car unique
    # donc on supprime manuellement 1 colonne de Sex et Embarked
    cols_to_drop = ["Sex_female", "Embarked_C"]
    X_train = X_train.drop(columns=cols_to_drop)

    if X_test is not None:
        X_test = pd.get_dummies(X_test, columns=categorical_cols, drop_first=False)
        # Réindexation pour garantir le même ordre des colonnes (pas garanti apres oh encodage)
        X_test = X_test.reindex(columns=st.session_state.columns, fill_value=0)
        X_test = X_test.drop(columns=cols_to_drop)

    return X_train, X_test, y_train, y_test


@st.cache_data
def to_display(df) -> pd.DataFrame:
    df_display = df.copy()
    df_display.columns = [
        "Survie",
        "Classe",
        "Nom",
        "Sexe",
        "Age",
        "Fratrie & Conjoint(e)",
        "Parents & Enfants",
        "Ticket",
        "Tarif",
        "Cabine",
        "Embarquement",
    ]
    df_display["Survie"].replace({1: "Oui", 0: "Non"}, inplace=True)
    df_display["Sexe"].replace({"male": "♂️ Homme", "female": "♀️ Femme"}, inplace=True)
    df_display["Embarquement"].replace(
        {"C": "🇫🇷 Cherbourg", "Q": "🇮🇪 Queenstown", "S": "🇬🇧 Southampton"}, inplace=True
    )
    df_display["Classe"].replace({1: "1ère", 2: "2ème", 3: "3ème"}, inplace=True)
    return df_display
