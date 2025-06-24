import streamlit as st
from utils import set_seed, load_csv, preprocess_data
import numpy as np
import pandas as pd

st.set_page_config(page_title="Titanic - Predictions")
st.header("Prédictions")

# URL de la vidéo
video_url = "https://www.youtube.com/watch?v=AzmdpGuIiZ4"

st.video(video_url)


set_seed()

st.subheader("Calculer les chances de survie des passagers")

model_choisi = st.selectbox(
    label="Choix du modèle",
    options=list(st.session_state.models.keys()),
)

if model_choisi is None:
    st.error("Aucun modèle à choisir")
    st.stop()
else:
    model = st.session_state[model_choisi]


set_seed()
df = load_csv()
X, _, y, _ = preprocess_data(df, split=False)


y_proba = model.predict_proba(X)
y_pred = model.predict(X)


df.insert(
    loc=0, column="chance de survie prédite", value=np.round(y_proba[:, 1] * 100, 2)
)
df = df.sort_values(by="chance de survie prédite", ascending=False)
df.insert(
    loc=2,
    column="Prédiction juste",
    value=y_pred == y,
)
df["Prédiction juste"] = df["Prédiction juste"].apply(lambda x: "✅" if x else "❌")

st.dataframe(df)
st.caption(
    f"Les chances de survie des passagers sont évaluées par prédiction du classifieur sélectionné ({model_choisi}) avec ses paramètres optimisés."
)

counts = df["Prédiction juste"].value_counts()
frequencies = df["Prédiction juste"].value_counts(normalize=True)
result = pd.DataFrame(
    {"Nb": counts, "%": np.round(100 * frequencies, 2).astype(str) + " %"}
)

st.write(result)

st.subheader("Calculer les chances de survie d'un passager ayant les caractéristiques de votre choix")


if st.button("Fin du voyage"):
    if len(st.session_state.pages) == 5:
        st.session_state.pages.append(
            st.Page("pages/6_Terminus.py", title="Terminus", icon="🏁")
        )
    st.switch_page(st.session_state.pages[5])

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
