import streamlit as st
from sklearn.utils import all_estimators
from utils import set_seed, load_csv, preprocess_data
import pandas as pd
import time
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
)

st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>📝 Evaluation</h2>",
    unsafe_allow_html=True,
)


st.subheader(
    (
        ":blue[Entraînement]"
        if st.session_state.lang.startswith("fr")
        else ":blue[Training]"
    ),
    divider=True,
)

set_seed()

# Récupérer tous les classifiers
all_classifiers = all_estimators(type_filter="classifier")

st.write(
    "Les différents modèles de Machine Learning de la librairie Scikit-learn sont entraînés avec leurs paramètres par défaut puis classés selon 3 scoring différents (balanced accuracy, ROC AUC et f1-score) calculés par Cross Validation à 5 folds sur un ensemble d’entraînement constitué de 80% des données disponibles."
    if st.session_state.lang.startswith("fr")
    else "The various Machine Learning models from the Scikit-learn library are trained with their default parameters, then ranked based on three different scoring metrics (balanced accuracy, ROC AUC, and F1-score), computed using 5-fold cross-validation on a training set composed of 80% of the available data."
)

df = load_csv()

X_train, X_test, y_train, y_test = preprocess_data(df, split=True)

# st.dataframe(X_train)
# st.dataframe(X_test)

# Récupérer tous les classifiers
all_classifiers = all_estimators(type_filter="classifier")

# warnings.filterwarnings("ignore")

results = []
errors = []
df_results = pd.DataFrame()

progress_bar = st.progress(0)
status = st.empty()
container = st.container()

total = len(all_classifiers)

placeholder = st.empty()


start_total_time = time.time()

skf = StratifiedKFold(n_splits=5, shuffle=True)

for i, (name, ClfClass) in enumerate(all_classifiers):

    progress_bar.progress((i + 1) / total)
    status.text(f"{i+1}/{total} - {name}")

    try:
        clf = ClfClass()
        start_time = time.time()

        bal_acc_scores = cross_val_score(
            clf, X_train, y_train, cv=skf, scoring="balanced_accuracy"
        )

        roc_auc_scores = f1_scores = cross_val_score(
            clf, X_train, y_train, cv=skf, scoring="roc_auc"
        )

        f1_scores = cross_val_score(clf, X_train, y_train, cv=skf, scoring="f1")

        bal_acc_mean = bal_acc_scores.mean()
        roc_auc_mean = roc_auc_scores.mean()
        f1_mean = f1_scores.mean()

        end_time = time.time()
        duration = int((end_time - start_time) * 1000)

        if pd.isna(bal_acc_mean) or pd.isna(roc_auc_mean) or pd.isna(f1_mean):
            raise ValueError("Scores invalides (nan)")

        results.append(
            {
                "Model": name,
                "Balanced Accuracy (%)": round(100 * bal_acc_mean, 2),
                "ROC AUC": roc_auc_mean,
                "f1-score": f1_mean,
                "Time (ms)": duration,
            }
        )
    except Exception as e:
        errors.append({"Model": name, "Error": e})

    # Afficher sous forme de DataFrame triée par Accuracy décroissante
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values(
        by="Balanced Accuracy (%)", ascending=False
    ).reset_index(drop=True)

    placeholder.dataframe(df_results)

duration = round(time.time() - start_total_time, 1)

status.text("")

container.success(
    f"{len(results)} "
    + (
        "modèles ont été évalués en"
        if st.session_state.lang.startswith("fr")
        else "models were evaluated in"
    )
    + f" {duration} s",
    icon="✅",
)

container.warning(
    f"{len(errors)} "
    + (
        "modèles n'ont pas pu être entraînés"
        if st.session_state.lang.startswith("fr")
        else "models could not be trained"
    ),
    icon="ℹ️",
)

st.caption(
    (
        "seed de la session = "
        if st.session_state.lang.startswith("fr")
        else "session seed = "
    )
    + f"{st.session_state.seed}"
)

with st.expander(
    "Afficher les erreurs"
    if st.session_state.lang.startswith("fr")
    else "Display errors"
):
    st.dataframe(errors)


best_model_name = df_results.iloc[0, 0]

st.subheader(":blue[Evaluation]", divider=True)

st.write(f"🏆 {best_model_name}")

st.write(
    f"Le modèle ayant obtenu les meilleures performances durant l'entraînement est {best_model_name}. Son évaluation est réalisée sur un ensemble de test de type hold-out, constitué de 20 % des données non utilisées lors de l'ajustement du modèle."
    if st.session_state.lang.startswith("fr")
    else f"The best-performing model during training was {best_model_name}. Its performance is evaluated on a hold-out test set comprising 20% of the data that was not used during model fitting."
)

for name, Clf in all_classifiers:
    if name == best_model_name:
        best_model = Clf()
        break
else:
    raise ValueError(f"Impossible de trouver {best_model_name} dans all_classifiers")

assert best_model is not None, f"best_model_name {best_model_name} non trouvé"

best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

balanced_acc = round(100 * balanced_accuracy_score(y_test, y_pred), 2)  # type: ignore
st.write(f"- Balanced accuracy = **{balanced_acc} %**")


# Afficher classification_report sous forme de DataFrame
report_dict = classification_report(y_test, y_pred, output_dict=True)  # type: ignore
df_report = pd.DataFrame(report_dict).transpose()
st.write("- Classification Report")
st.dataframe(df_report)

# Afficher la matrice de confusion
cm = confusion_matrix(y_test, y_pred)  # type: ignore
df_cm = pd.DataFrame(cm, index=["Actual 0", "Actual 1"], columns=["Pred 0", "Pred 1"])
st.write("- Confusion Matrix")
st.dataframe(df_cm)


_, col, _ = st.columns(3)
with col:
    st.write("")
    st.write("")
    st.page_link(
        st.Page(
            "pages/4_Optimisation.py",
            title=(
                "Passer à l'étape suivante"
                if st.session_state.lang.startswith("fr")
                else "Go to the next step"
            ),
            icon="➡️",
        )
    )
st.divider()
st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
