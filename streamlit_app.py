# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": """
## Titanic Survival Predictor  
Ce projet prédit les chances de survie des passagers du Titanic grâce au **machine learning**.  

🔍 Code source : [GitHub](https://github.com/DidierFlamm/titanic-survival-predictor)  
✉️ Contact : [didier.flamm@gmail.com](mailto:didier.flamm@gmail.com)  
🔗 LinkedIn : [didier-flamm](https://www.linkedin.com/in/didier-flamm)  
📁 Portfolio : [Streamlit Community Cloud](https://share.streamlit.io/user/didierflamm)  

© 2025 Didier Flamm
""",
    }
)

st.logo(
    "https://img.icons8.com/?size=100&id=s5NUIabJrb4C&format=png&color=000000",
    size="large",
)
st.sidebar.header("Settings", divider=True)
st.sidebar.subheader("Musique")
mp3_url = "https://archive.org/download/celine-dion-my-heart-will-go-on_202207/Celine%20Dion%20-%20My%20Heart%20Will%20Go%20On.mp3"
st.sidebar.audio(
    mp3_url,
    format="audio/mp3",
    loop=False,
    autoplay=True,
)


if "pages" not in st.session_state:
    st.session_state.pages = [
        st.Page("pages/1_Accueil.py", title="Accueil", icon="⚓", default=True),
        # st.Page("pages/2_Visualisation.py", title="Visualisation", icon="📊"),
        # st.Page("pages/3_Evaluation.py", title="Evaluation", icon="📝"),
        # st.Page("pages/4_Optimisation.py", title="Optimisation", icon="📈"),
    ]

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

pg = st.navigation(st.session_state.pages, position="top")
pg.run()
