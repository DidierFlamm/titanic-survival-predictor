# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.logo(
    # "https://raw.githubusercontent.com/DidierFlamm/DidierFlamm/main/dids.webp",
    "https://img.icons8.com/?size=100&id=s5NUIabJrb4C&format=png&color=000000",
    size="large",
)


st.sidebar.subheader("Language", divider=True)

iso_639_1_url = "https://raw.githubusercontent.com/DidierFlamm/titanic-survival-predictor/refs/heads/main/data/languages.csv"
languages = pd.read_csv(iso_639_1_url)

default_lang = "fr-FR"
default_index = languages[languages.loc[:, "lang"] == default_lang].index[0]
language = st.sidebar.selectbox(
    "Select language", options=languages, index=int(default_index)
)

lang = languages.loc[languages["language"] == language, "lang"].values[0]

st.session_state.lang = lang

st.sidebar.subheader("Ambiance", divider=True)

ambiance = st.sidebar.radio("Select ambiance", ("🎛️ Trance remix", "💿 Titanic OST"))

if ambiance.startswith("🎛️"):
    iframe_code = """<iframe width="100%" height="130" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1851039789&color=%231a4b75&auto_play=true&hide_related=True&show_comments=false&show_user=false&show_reposts=false&show_teaser=false"></iframe>"""
    # """<iframe width="100%" height="130" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/97158016&color=%231a4b75&auto_play=true&hide_related=false&show_comments=false&show_user=false&show_reposts=false&show_teaser=false"></iframe>"""
    with st.sidebar:
        components.html(iframe_code, height=120)
else:
    tracks = {
        "1. Never an Absolution": "https://archive.org/download/TitanicMusicfromtheMotionPicture/01%20Never%20an%20Absolution.mp3",
        "2. Distant Memories": "https://archive.org/download/TitanicMusicfromtheMotionPicture/02%20Distant%20Memories.mp3",
        "3. Southampton": "https://archive.org/download/TitanicMusicfromtheMotionPicture/03%20Southampton.mp3",
        "4. Rose": "https://archive.org/download/TitanicMusicfromtheMotionPicture/04%20Rose.mp3",
        "5. Leaving Port": "https://archive.org/download/TitanicMusicfromtheMotionPicture/05%20Leaving%20Port.mp3",
        '6. "Take Her to Sea, Mr. Murdoch"': "https://archive.org/download/TitanicMusicfromtheMotionPicture/06%20%22Take%20Her%20to%20Sea%2C%20Mr.%20Murdoch%22.mp3",
        '7. "Hard to Starboard"': "https://archive.org/download/TitanicMusicfromtheMotionPicture/07%20Track07.mp3",
        "8. Unable to Stay, Unwilling to Leave": "https://archive.org/download/TitanicMusicfromtheMotionPicture/08%20Unable%20to%20Stay%2C%20Unwilling%20to%20Leave.mp3",
        "9. The Sinking": "https://archive.org/download/TitanicMusicfromtheMotionPicture/09%20The%20Sinking.mp3",
        "10. Death of Titanic": "https://archive.org/download/TitanicMusicfromtheMotionPicture/10%20Death%20of%20Titanic.mp3",
        "11. A Promise Kept": "https://archive.org/download/TitanicMusicfromtheMotionPicture/11%20A%20Promise%20Kept.mp3",
        "12. A Life So Changed": "https://archive.org/download/TitanicMusicfromtheMotionPicture/12%20A%20Life%20So%20Changed.mp3",
        "13. An Ocean of Memories": "https://archive.org/download/TitanicMusicfromtheMotionPicture/13%20An%20Ocean%20of%20Memories.mp3",
        "14. My Heart Will Go On": "https://archive.org/download/TitanicMusicfromtheMotionPicture/14%20My%20Heart%20Will%20Go%20On.mp3",
        "15. Hymn to the Sea": "https://archive.org/download/TitanicMusicfromtheMotionPicture/15%20Hymn%20to%20the%20Sea.mp3",
    }

    if "track_index" not in st.session_state:
        st.session_state.track_index = 0

    track = st.sidebar.selectbox(
        "Select track",
        list(tracks.keys()),
        index=st.session_state.track_index,
    )

    st.session_state.track_index = list(tracks.keys()).index(track)

    st.sidebar.audio(
        tracks[track],
        format="audio/mpeg",  # = mp3
        autoplay=True,
    )


st.sidebar.subheader("View all apps", divider=True)
# st.sidebar.markdown(
#    """
# <div style='text-align: center'>
#  <a href="https://share.streamlit.io/user/didierflamm" target="_blank">
#    <img src="https://raw.githubusercontent.com/DidierFlamm/DidierFlamm/main/dids.webp" style="max-width: 100%; height: auto;" width="150"/>
#  </a>
# </div>
# """,
#    unsafe_allow_html=True,
# )

st.sidebar.image(
    "https://raw.githubusercontent.com/DidierFlamm/DidierFlamm/main/dids.webp"
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
        st.Page("pages/2_Visualisation.py", title="Visualisation", icon="📊"),
        st.Page("pages/3_Evaluation.py", title="Evaluation", icon="📝"),
        st.Page("pages/4_Optimisation.py", title="Optimisation", icon="📈"),
        st.Page("pages/5_Predictions.py", title="Predictions", icon="🎯"),
        st.Page("pages/6_Terminus.py", title="Terminus", icon="🏁"),
    ]

pg = st.navigation(st.session_state.pages, position="top")
pg.run()
