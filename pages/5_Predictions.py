import streamlit as st
from utils import set_seed, load_csv


st.set_page_config(page_title="Titanic - Predictions")
st.header("Prédictions")


set_seed()

model_choisi = st.selectbox(
    label="Choix du modèle",
    options=[
        "Logistic Regression",
        "K-Neighbors",
        "SVC",
        "Random Forest",
        "Gradient Boosting",
    ],
)

df = load_csv()
df.insert(0, "Chance de survie (%)", "🚧")
df = df.sort_values(by=["Chance de survie (%)", "#"], ascending=[False, True])
st.dataframe(df)
st.caption(
    f"Les chances de survie des passagers sont évaluées par les prédictions du classifieur {model_choisi} optimisé."
)

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
