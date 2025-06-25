import streamlit as st
from utils import set_seed, load_csv, preprocess_data
import numpy as np
import pandas as pd

st.header("🎯 Prédictions" if st.session_state.lang == "fr" else "🎯 Predictions")

# URL de la vidéo
video_url = "https://youtu.be/vXBY6Zu46HE"

st.video(video_url, autoplay=True, muted=True)


set_seed()

st.subheader(
    "Comparer les chances de survie des passagers"
    if st.session_state.lang == "fr"
    else "Compare passengers’ chances of survival"
)

st.write(
    "Les chances de survie des passagers sont évaluées par prédiction de probabilité du classifieur optimisé :"
    if st.session_state.lang == "fr"
    else "The chances of survival are assessed by the optimized classifier’s probability prediction:"
)

st.write(
    """- une probabilité supérieure ou égale à 50% prédit la survie du passager,
- une probabilité inférieure à 50% prédit la non survie du passager."""
    if st.session_state.lang == "fr"
    else """- a probability greater than or equal to 50% predicts passenger survival,  
- a probability less than 50% predicts passenger non-survival."""
)

model_choisi = st.selectbox(
    label="Choisir le modèle" if st.session_state.lang == "fr" else "Choose the model",
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


st.divider()

st.subheader(
    "Évaluer les chances de survie d'un passager personnalisé"
    if st.session_state.lang == "fr"
    else "Evaluate the survival chances of a custom passenger"
)


# il faudra activer le calcul de la proba via l'argument on_change des widgets

col1, col2 = st.columns(2, border=True)

with col1:
    sexe = st.radio("**Sexe**", ("Femme", "Homme"), horizontal=True)

    age = st.slider("**Age**", 0, 100, 50)

    pclass = st.selectbox("**Classe**", options=[1, 2, 3], index=2)

    fare = st.slider("**Tarif**", 0, 100, 50)

    embarked = st.selectbox(
        "**Port d'embarquement**",
        options=["🇫🇷 Cherbourg", "🇮🇪 Queenstown", "🇬🇧 Southampton"],
        index=0,
    )


with col2:
    st.write("*Famille du passager à bord :*")

    nb_siblings = st.selectbox("**• Frères et sœurs**", options=range(11), index=0)

    has_spouse = st.radio("**• Époux(se)**", ("Oui", "Non"), horizontal=True)

    nb_parents = st.selectbox("**• Parents**", options=[0, 1, 2], index=0)

    nb_children = st.selectbox("**• Enfants**", options=range(11), index=0)

st.write("🚧 WIP 🎯 Prédiction du modèle : 🟢 ou 🔴 (probabilité de survie = ### %) 🚧")


st.divider()

if len(st.session_state.pages) == 5:
    st.session_state.pages.append(
        st.Page("pages/6_Terminus.py", title="Terminus", icon="🏁")
    )
    st.navigation(st.session_state.pages, position="top")

st.page_link(
    st.Page(
        "pages/6_Terminus.py",
        title=(
            "Passer à l'étape suivante"
            if st.session_state == "fr"
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
