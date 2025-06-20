# -*- coding: utf-8 -*-
import streamlit as st

st.sidebar.header("Settings", divider=True)
st.sidebar.subheader("Musique")
mp3_url = "https://archive.org/download/celine-dion-my-heart-will-go-on_202207/Celine%20Dion%20-%20My%20Heart%20Will%20Go%20On.mp3"
st.sidebar.audio(
    mp3_url,
    format="audio/mp3",
    loop=True,
    autoplay=True,
)


if "pages" not in st.session_state:
    st.session_state.pages = [
        st.Page("pages/1_Accueil.py", title="Accueil", icon="🛳️", default=True)
    ]

# st.session_state.pages est incrémenté par les boutons en fin de chaque page

pg = st.navigation(st.session_state.pages, position="top")
pg.run()


st.sidebar.divider()
st.sidebar.markdown(
    """
<div style='text-align: center;margin-top: 150px;'>
  <a href="https://share.streamlit.io/user/didierflamm" target="_blank">
    <img src="https://raw.githubusercontent.com/DidierFlamm/DidierFlamm/main/dids.webp" style="max-width: 100%; height: auto;" width="150"/>
  </a>
</div>
""",
    unsafe_allow_html=True,
)
