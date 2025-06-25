# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components

st.logo(
    # "https://raw.githubusercontent.com/DidierFlamm/DidierFlamm/main/dids.webp",
    "https://img.icons8.com/?size=100&id=s5NUIabJrb4C&format=png&color=000000",
    size="large",
)


st.sidebar.subheader("Language", divider=True)

language = st.sidebar.selectbox(
    "Select language", options=["🇫🇷 Français", "🇬🇧 English"], index=0
)

lang = "fr" if language.startswith("🇫🇷") else "en"
st.session_state.lang = lang

st.sidebar.subheader("Ambiance", divider=True)

iframe_code = """<iframe width="100%" height="130" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1851039789&color=%231a4b75&auto_play=true&hide_related=false&show_comments=false&show_user=false&show_reposts=false&show_teaser=false"></iframe></div>"""
# """<iframe width="100%" height="130" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/97158016&color=%231a4b75&auto_play=true&hide_related=false&show_comments=false&show_user=false&show_reposts=false&show_teaser=false"></iframe><div style="font-size: 10px; color: #cccccc;line-break: anywhere;word-break: normal;overflow: hidden;white-space: nowrap;text-overflow: ellipsis; font-family: Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif;font-weight: 100;"></div>"""


with st.sidebar:
    components.html(iframe_code, height=120)

st.sidebar.subheader("View all apps", divider=True)
st.sidebar.markdown(
    """
<div style='text-align: center'>
  <a href="https://share.streamlit.io/user/didierflamm" target="_blank">
    <img src="https://raw.githubusercontent.com/DidierFlamm/DidierFlamm/main/dids.webp" style="max-width: 100%; height: auto;" width="150"/>
  </a>
</div>
""",
    unsafe_allow_html=True,
)

st.set_page_config(
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": (
            """## Titanic Survival Predictor  
Ce projet prédit les chances de survie des passagers du Titanic grâce au **machine learning**. Le code source est disponible sur  
"""
            if st.session_state.lang == "fr"
            else """## Titanic Survival Predictor  
This project predicts the survival chances of Titanic passengers using machine learning. The source code is available on """
        )
        + """[GitHub](https://github.com/DidierFlamm/titanic-survival-predictor)  

© 2025 Didier Flamm  
✉️ [didier.flamm@gmail.com](mailto:didier.flamm@gmail.com) – 🔗 [LinkedIn](https://www.linkedin.com/in/didier-flamm) – 📁 [Portfolio](https://share.streamlit.io/user/didierflamm)  
""",
    }
)

if "pages" not in st.session_state:
    st.session_state.pages = [
        st.Page(
            "pages/1_Home.py",
            title="Home",
            icon="⚓",
            default=True,
        ),
        # st.Page("pages/2_Visualisation.py", title="Visualisation", icon="📊"),
        # st.Page("pages/3_Evaluation.py", title="Evaluation", icon="📝"),
        # st.Page("pages/4_Optimisation.py", title="Optimisation", icon="📈"),
    ]

pg = st.navigation(st.session_state.pages, position="top")
pg.run()
