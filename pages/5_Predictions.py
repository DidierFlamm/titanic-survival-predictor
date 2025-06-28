import streamlit as st
from utils import set_seed, load_csv, preprocess_data, get_fare_bounds
import numpy as np
import pandas as pd

st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>🎯 Predictions</h2>",
    unsafe_allow_html=True,
)

if "df_results" not in st.session_state:
    st.info(
        """Les modèles doivent être optimisés avant de pouvoir réaliser des prédictions fiables.  
        Veuillez vous rendre à l'étape 📈 Optimisation en cliquant sur le bouton ci-dessous :""",
        icon="ℹ️",
    )
    st.page_link(
        st.Page(
            "pages/4_Optimisation.py",
            title="Optimisation",
            icon="📈",
        )
    )
    st.stop()

# URL de la vidéo
video_url = "https://youtu.be/vXBY6Zu46HE"

st.video(video_url, autoplay=True, muted=True)


set_seed()

st.subheader(
    (
        ":blue[Chances de survie des passagers]"
        if st.session_state.lang.startswith("fr")
        else ":blue[Survival chances of passengers]"
    ),
    divider=True,
)

st.write(
    "Les chances de survie des passagers sont prédites par un modèle optimisé avec :"
    if st.session_state.lang.startswith("fr")
    else "The chances of survival are predicted by an optimized model with :"
)

st.write(
    """🟢 probabilité ≥ 50% : le passager survit  
🔴 probabilité < 50% : le passager ne survit pas"""
    if st.session_state.lang.startswith("fr")
    else """🟢 probability ≥ 50%: the passenger survives  
🔴 probability < 50%: the passenger does not survive"""
)


model_choisi = st.selectbox(
    label=(
        "Choisir le modèle"
        if st.session_state.lang.startswith("fr")
        else "Choose the model"
    ),
    options=list(st.session_state.df_results.Model),
)

if model_choisi is None:
    st.error("Aucun modèle à choisir")
    st.stop()
else:
    model = st.session_state[model_choisi]

st.write(
    f"📌 balanced accuracy of {model_choisi} model = **{st.session_state.df_results.loc[st.session_state.df_results.Model == model_choisi, "Balanced Accuracy"
].values[0]} %**"
)

set_seed()
df = load_csv(drop_outliers=True)
X, _, y, _ = preprocess_data(df, split=False)


y_proba = model.predict_proba(X)
y_pred = model.predict(X)


df.insert(loc=0, column="Chance de survie", value=np.round(y_proba[:, 1] * 100, 2))
df = df.sort_values(by="Chance de survie", ascending=False)
df.insert(
    loc=2,
    column="Prédiction juste",
    value=y_pred == y,
)
df["Survived"] = df["Survived"].apply(lambda x: "🟢" if x else "🔴")
df["Prédiction juste"] = df["Prédiction juste"].apply(lambda x: "✔️" if x else "❌")

st.dataframe(df)

st.caption(f"seed de la session = {st.session_state.seed}")

counts = df["Prédiction juste"].value_counts()
frequencies = df["Prédiction juste"].value_counts(normalize=True)
result = pd.DataFrame(
    {"Nb": counts, "%": np.round(100 * frequencies, 2).astype(str) + " %"}
)

st.dataframe(result)


st.subheader(
    (
        ":blue[Chance de survie d'un passager personnalisé]"
        if st.session_state.lang.startswith("fr")
        else ":blue[Survival chance of a custom passenger]"
    ),
    divider=True,
)


# il faudra activer le calcul de la proba via l'argument on_change des widgets

col1, col2 = st.columns(2, border=True)

bounds = get_fare_bounds(df)

with col1:

    st.markdown(
        """<div style="text-align: center;"><em>Caractéristiques du passager</em></div>""",
        unsafe_allow_html=True,
    )
    st.write("")

    sexe = st.radio(
        "**Sexe**",
        ("female", "male"),
        format_func=lambda x: "Femme" if x == "female" else "Homme",
        horizontal=True,
    )

    age = st.slider("**Age**", 0, 100, 50)

    pclass = st.radio("**Classe**", (1, 2, 3), horizontal=True)

    fare = st.slider(
        "**Tarif**",
        int(bounds[pclass]["min"]),
        int(bounds[pclass]["max"]),
        int(bounds[pclass]["median"]),
    )

    st.caption("tarif par défaut = valeur médiane de la classe")

    embarked = st.selectbox(
        "**Port d'embarquement**",
        options=["C", "Q", "S"],
        index=0,
        format_func=lambda x: {
            "C": "🇫🇷 Cherbourg",
            "Q": "🇮🇪 Queenstown",
            "S": "🇬🇧 Southampton",
        }[x],
    )


with col2:
    st.markdown(
        """<div style="text-align: center;"><em>Famille du passager (à bord du Titanic)</em></div>""",
        unsafe_allow_html=True,
    )
    st.write("")

    spouse = st.radio(
        "**Époux(se)**",
        [1, 0],
        format_func=lambda x: "Oui" if x else "Non",
        horizontal=True,
    )

    siblings = st.slider("**Frères et sœurs**", 0, 10, 0)

    parents = st.radio("**Parents**", (0, 1, 2), horizontal=True)

    children = st.slider("**Enfants**", 0, 10, 0)

custom = pd.DataFrame(
    [
        [
            pclass,
            sexe,
            age,
            spouse + siblings,
            parents + children,
            fare,
            embarked,
        ]
    ],
    columns=["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"],
)
custom.index = ["Passenger"]  # type: ignore
# st.dataframe(custom)


set_seed()
X, _, _, _ = preprocess_data(custom, split=False)
# st.dataframe(X)
model = st.session_state[model_choisi]
y_prob = model.predict_proba(X)

chance = round(100 * y_prob[0, 1], 2)

st.metric(
    "Survival chance predicted",
    ("🟢" if chance >= 50 else "🔴") + f" {chance} %",
)

_, col, _ = st.columns(3)
with col:
    st.write("")
    st.write("")
    st.page_link(
        st.Page(
            "pages/6_Arrival.py",
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
