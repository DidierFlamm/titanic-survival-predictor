import streamlit as st


st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>🏁 Terminus</h2>",
    unsafe_allow_html=True,
)


st.balloons()

# URL de la vidéo
video_url = "https://youtu.be/Sj9MEwjkxE0"

st.video(video_url, autoplay=True, muted=True)

st.write("🚧 WIP")
st.write("merci ...")

st.markdown(
    'Le code source est disponible sur <a href="https://github.com/DidierFlamm/titanic-survival-predictor" target="_blank">GitHub</a>',
    unsafe_allow_html=True,
)


st.markdown(
    'Retrouvez toutes mes applis interactives sur <a href="https://share.streamlit.io/user/didierflamm" target="_blank">Streamlit Community Cloud</a>',
    unsafe_allow_html=True,
)

st.write("WIP 🚧")

st.divider()
st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
