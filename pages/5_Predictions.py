import streamlit as st
from utils import set_seed, load_csv, preprocess_data
import numpy as np
import pandas as pd

st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>🎯 Predictions</h2>",
    unsafe_allow_html=True,
)

if "df_results" not in st.session_state:
    st.warning(
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
        else ":blue[Passengers’ chances of survival]"
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
    f"📌 balanced accuracy = **{st.session_state.df_results.loc[st.session_state.df_results.Model == model_choisi, "Balanced Accuracy"
].values[0]} %**"
)

set_seed()
df = load_csv()
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
df["Prédiction juste"] = df["Prédiction juste"].apply(lambda x: "✅" if x else "❌")

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
        ":blue[Chance de survie d'un passager 'personnalisé']"
        if st.session_state.lang.startswith("fr")
        else ":blue[Survival chance of a custom passenger]"
    ),
    divider=True,
)


# il faudra activer le calcul de la proba via l'argument on_change des widgets

col1, col2 = st.columns(2, border=True)

with col1:

    st.markdown(
        """<div style="text-align: center;"><em>Caractéristiques du passager</em></div>""",
        unsafe_allow_html=True,
    )

    st.divider()

    sexe = st.radio("**Sexe**", ("Femme", "Homme"), horizontal=True)

    age = st.slider("**Age**", 0, 100, 50)

    pclass = st.radio("**Classe**", (1, 2, 3), horizontal=True)

    fare = st.slider("**Tarif**", 0, 100, 50)

    embarked = st.selectbox(
        "**Port d'embarquement**",
        options=["🇫🇷 Cherbourg", "🇮🇪 Queenstown", "🇬🇧 Southampton"],
        index=0,
    )


with col2:
    st.markdown(
        """<div style="text-align: center;"><em>Famille du passager à bord du Titanic</em></div>""",
        unsafe_allow_html=True,
    )
    st.divider()

    spouse = st.checkbox("**Époux(se)**")

    nb_siblings = st.slider("**Frères et sœurs**", 0, 10, 0)

    nb_parents = st.radio("**Parents**", (0, 1, 2), horizontal=True)

    nb_children = st.slider("**Enfants**", 0, 10, 0)

st.write("🚧 WIP 🎯 Prédiction du modèle : 🟢 ou 🔴 (probabilité de survie = ### %) 🚧")


_, col, _ = st.columns(3)
with col:
    st.write("")
    st.write("")
    st.page_link(
        st.Page(
            "pages/6_Terminus.py",
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
