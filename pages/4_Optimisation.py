import streamlit as st
import time
from utils import set_seed, load_csv, preprocess_data
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import balanced_accuracy_score
import pandas as pd


st.header("📈 Optimisation")


st.subheader("🔧 Fine tuning")
st.write(
    "Optimisation des hyperparamètres de 5 modèles par Grid Search Cross Validation sur l'ensemble d'entraînement (80% des données) :"
    if st.session_state.lang == "fr-FR"
    else "Hyperparameter tuning of 5 models using Grid Search Cross Validation on the training set (80% of the data) :"
)

models = {
    "Logistic Regression": LogisticRegression(),
    "K-Neighbors": KNeighborsClassifier(),
    "SVC": SVC(probability=True),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
}

for model_name in models:
    st.write(f"- {model_name}")

set_seed()
df = load_csv()

X_train, X_test, y_train, y_test = preprocess_data(df, split=True)


params = {
    "Logistic Regression": {
        "C": [0.01, 0.1, 1, 10],
        "penalty": ["l2"],
        "solver": ["lbfgs"],
    },
    "K-Neighbors": {
        "n_neighbors": [3, 5, 7],
        "weights": ["uniform", "distance"],
    },
    "SVC": {
        "C": [0.1, 1, 10],
        "kernel": ["linear", "rbf"],
        "gamma": ["scale", "auto"],
    },
    "Random Forest": {
        "n_estimators": [50, 100],
        "max_depth": [None, 5, 10],
        "min_samples_split": [2, 5],
    },
    "Gradient Boosting": {
        "n_estimators": [50, 100],
        "learning_rate": [0.01, 0.1],
        "max_depth": [3, 5],
    },
}

with st.expander("Afficher les paramètres de la grille de recherche"):
    st.json(params)

progress_bar = st.progress(0)
status = st.empty()
placeholder = st.empty()

start_total_time = time.time()

st.subheader("🎯 Résultats" if st.session_state.lang == "fr-FR" else "🎯 Results")

st.write(
    "L'évaluation de chaque modèle est réalisée sur l'ensemble de test (20% des données)."
    if st.session_state.lang == "fr-FR"
    else "Each model is evaluated on the test set (20% of the data)."
)

best_models = {}
results = []


for idx, name in enumerate(models):

    progress_bar.progress((idx + 1) / len(models))
    status.text(f"{idx+1}/{len(models)} - {name}")

    # print(f"🔍 GridSearch for {name}...")
    grid = GridSearchCV(
        models[name], params[name], cv=5, n_jobs=-1, scoring="balanced_accuracy"
    )
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_

    st.session_state[name] = best_model

    y_pred = best_model.predict(X_test)

    bal_acc = round(100 * balanced_accuracy_score(y_test, y_pred), 2)  # type: ignore

    st.markdown(
        f"""
- **{name}**  
    Best Params : {grid.best_params_}  
    Balanced Accuracy : **{bal_acc} %**  
"""
    )

    results.append(
        {
            "Model": name,
            "Balanced Accuracy": bal_acc,
            "Best Params": grid.best_params_,
        }
    )
    with st.expander(
        "Afficher les détails de la Grid Search CV"
        if st.session_state.lang == "fr-FR"
        else "Display the grid search parameters"
    ):
        st.dataframe(pd.DataFrame(grid.cv_results_))

st.divider()

duration = round(time.time() - start_total_time, 1)

status.text("")

placeholder.success(
    (
        f"Les {len(models)} modèles ont été optimisés en {duration} s"
        if st.session_state.lang == "fr-FR"
        else f"The {len(models)} models were optimized in {duration} seconds."
    ),
    icon="✅",
)

st.subheader("🏆 Classement" if st.session_state.lang == "fr-FR" else "🏆 Ranking")

df_results = pd.DataFrame(results).sort_values(by="Balanced Accuracy", ascending=False)

df_results.index = range(1, 6)  # type: ignore

st.dataframe(df_results)

st.caption(f"seed de la session = {st.session_state.seed}")

if "df_results" not in st.session_state:
    st.session_state.df_results = df_results

st.divider()

if len(st.session_state.pages) == 4:
    st.session_state.pages.append(
        st.Page("pages/5_Predictions.py", title="Predictions", icon="🎯")
    )
    st.navigation(st.session_state.pages, position="top")

st.page_link(
    st.Page(
        "pages/5_Predictions.py",
        title=(
            "Passer à l'étape suivante"
            if st.session_state.lang == "fr-FR"
            else "Go to the next step"
        ),
        icon="➡️",
    )
)

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
