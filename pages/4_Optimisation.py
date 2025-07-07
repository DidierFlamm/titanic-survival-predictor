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

st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>📈 Optimisation</h2>",
    unsafe_allow_html=True,
)


st.subheader("🔧 :blue[Fine tuning]", divider=True)
st.write(
    "L'optimisation des hyperparamètres de 5 modèles est réalisée par Grid Search Cross Validation sur l'ensemble d'entraînement (80% des données) :"
    if st.session_state.lang.startswith("fr")
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
df = load_csv(drop_outliers=True)

X_train, X_test, y_train, y_test = preprocess_data(df, split=True)

# memorize les colonnes pour pouvoir réindexer le X custom qui n'aura pas toutes les colones OH
if "columns" not in st.session_state:
    st.session_state.columns = X_train.columns

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

with st.expander("🔍 Afficher les détails"):
    st.json(params)

progress_bar = st.progress(0)
status_placeholder = st.empty()
status_placeholder.text(f"0/{len(models)}")
success_placeholder = st.empty()


start_total_time = time.time()


best_models = {}
results = []


for idx, name in enumerate(models):

    with st.spinner(f"Optimizing {name}", show_time=True):

        progress_bar.progress((idx) / len(models))
        status_placeholder.text(f"{idx+1}/{len(models)} - optimizing {name}")

        grid = GridSearchCV(
            models[name], params[name], cv=5, n_jobs=-1, scoring="balanced_accuracy"
        )
        grid.fit(X_train, y_train)

        best_model = grid.best_estimator_

        st.session_state[name] = best_model

        y_pred = best_model.predict(X_test)

        # On récupère les résultats de la GridSearch sous forme de DataFrame
        cv_results = pd.DataFrame(grid.cv_results_)
        # Sélection de la ligne avec le meilleur rang (1)
        best_result = cv_results[cv_results["rank_test_score"] == 1]
        # Récupération du score moyen de test (balanced accuracy ici)
        best_mean_score = best_result["mean_test_score"].values[0]

        st.markdown(
            f"""
        - **{name}**  
            Best Params : {grid.best_params_}  
            Best Mean Balanced Accuracy : **{round(100*best_mean_score,2)} %**  
        """
        )

        assert y_test is not None
        # y_test is not none with preprocess_data(df, split=True)

        bal_acc = round(100 * balanced_accuracy_score(y_test, y_pred), 2)

        results.append(
            {
                "Model": name,
                "Balanced Accuracy": bal_acc,
                "Best Params": grid.best_params_,
            }
        )
        with st.expander(
            "📊 Afficher les résultats de la Grid Search CV"
            if st.session_state.lang.startswith("fr")
            else "📊 Display grid search results"
        ):
            st.dataframe(pd.DataFrame(grid.cv_results_))

duration = round(time.time() - start_total_time, 1)

progress_bar.progress(1.0)
status_placeholder.text("")

success_placeholder.success(
    (
        f"Les {len(models)} modèles ont été optimisés en {duration} s"
        if st.session_state.lang.startswith("fr")
        else f"The {len(models)} models were optimized in {duration} seconds."
    ),
    icon="✅",
)

st.subheader(
    (
        "🏆 :blue[Classement]"
        if st.session_state.lang.startswith("fr")
        else "🏆 :blue[Ranking]"
    ),
    divider=True,
)

st.write(
    "L'évaluation finale des modèles optimisés est réalisée sur l'ensemble de test (20% des données restantes)."
    if st.session_state.lang.startswith("fr")
    else "Each model is evaluated on the test set (20% of the data)."
)

df_results = pd.DataFrame(results).sort_values(by="Balanced Accuracy", ascending=False)

df_results.index = pd.Index(range(1, 6))

st.dataframe(df_results)

st.caption(f"seed de la session = {st.session_state.seed}")

if "df_results" not in st.session_state:
    st.session_state.df_results = df_results


_, col, _ = st.columns(3)
with col:
    st.write("")
    st.write("")
    st.page_link(
        st.Page(
            "pages/5_Predictions.py",
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
