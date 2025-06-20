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

# set title
st.set_page_config(page_title="Titanic - Optimisation")

# add next page
if len(st.session_state.pages) == 4:
    st.session_state.pages.append(
        st.Page("pages/5_Predictions.py", title="Prédictions", icon="🎯")
    )

# manage switch
if "go_next_4" in st.session_state:
    if st.session_state.go_next_4:
        st.session_state.go_next_4 = False
        st.switch_page(st.session_state.pages[4])


st.header("Optimisation")


st.subheader("🔧 Fine tuning")
st.write(
    "Optimisation des hyperparamètres de 5 modèles par Grid Search Cross-Validation"
)

set_seed()
df = load_csv()

X_train, X_test, y_train, y_test = preprocess_data(df)

models = {
    "Logistic Regression": LogisticRegression(),
    "K-Neighbors": KNeighborsClassifier(),
    "SVC": SVC(probability=True),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
}

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

st.write(
    "Cliquer ci-dessous pour développer l'arborescence de la grille de recherche :"
)
st.json(params, expanded=False)

progress_bar = st.progress(0)
status = st.empty()
placeholder = st.empty()

start_total_time = time.time()

st.subheader("🎯 Résultats")

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

    bal_acc = balanced_accuracy_score(y_test, y_pred)

    st.markdown(
        f"""
- **{name}**  
    Best Params : {grid.best_params_}  
    Balanced Accuracy : **{bal_acc:.4f}**  
"""
    )

    results.append(
        {
            "Model": name,
            "Balanced Accuracy": bal_acc,
            "Best Params": grid.best_params_,
        }
    )
    with st.expander("Afficher les détails"):
        st.dataframe(pd.DataFrame(grid.cv_results_))

    st.divider()

duration = round(time.time() - start_total_time, 1)

status.text("")

placeholder.success(
    f"{len(models)} modèles ont été optimisés avec succès en {duration} s", icon="✅"
)

st.subheader("🏆 Classement")

df_results = (
    pd.DataFrame(results)
    .sort_values(by="Balanced Accuracy", ascending=False)
    .reset_index(drop=True)
)
st.dataframe(df_results)

st.session_state.go_next_4 = True

st.button("Passer à l'étape suivante")


st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
