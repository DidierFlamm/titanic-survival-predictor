import streamlit as st

st.set_page_config(page_title="Titanic - Terminus")


st.header("Fin du voyage")

st.balloons()

st.write("merci ...")

# URL de la vidéo
video_url = "https://www.youtube.com/watch?v=RixBp7MSB2k"

st.video(video_url, autoplay = True, muted = True)

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray; margin-top: 50px;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
