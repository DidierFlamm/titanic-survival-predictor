# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_javascript import st_javascript
import pandas as pd
import time


st.logo(
    "https://img.icons8.com/?size=100&id=s5NUIabJrb4C&format=png&color=000000",
    size="large",
)

st.sidebar.subheader("Language", divider=True)

# récupération auto de la langue par défaut du navigateur en JS avec navigator.language

default_language_js = st_javascript("navigator.language")

disabled = False

if "default_language" not in st.session_state:
    if "google_credentials" not in st.secrets:
        st.session_state.default_language = (
            "fr-FR"  # fallback si pas de clé Google Traduction et disable selectbox
        )
        disabled = True
    elif default_language_js != 0:
        # cas où le language par défaut est récupéré par JS (valeur par défaut = 0 au 1er run)
        st.session_state.default_language = default_language_js

# Initialisation du selectbox en sync avec default_language
if "lang" not in st.session_state:
    try:
        st.session_state.lang = st.session_state.default_language
    except AttributeError:
        # attend que navigator.language récupère le langage par défaut
        time.sleep(0.1)
        st.rerun()

languages_csv = "https://raw.githubusercontent.com/DidierFlamm/titanic-survival-predictor/refs/heads/main/data/languages.csv"
languages = pd.read_csv(languages_csv)

st.sidebar.selectbox(
    "Select language",
    options=languages.lang,
    key="lang",
    format_func=lambda x: languages.loc[languages["lang"] == x, "language"].values[0],  # type: ignore
    label_visibility="collapsed",
    disabled=disabled,
)


flag = languages.loc[languages.lang == st.session_state.lang, "flag"].values[0]  # type: ignore
st.session_state.flag = flag

st.sidebar.subheader("Ambiance", divider=True)

ambiance = st.sidebar.radio(
    "Select ambiance",
    ("🔇 Silent mode", "😎 Summer version", "💿 Titanic OST"),
    label_visibility="collapsed",
)

trance_url = "https://mstore.pics/download?data=Q0t5My9HMkFCU0pQZnZpWk1MTXJISEo2V20vMTVkNiszWVRLTkIxVERaczlSUk1LYi9Jb2Q5cHRsR05NcVhhL2ozUUF3dElnUG5oNXVKSWtrZ0MvRnBuWDRJS3J6VG4vRDREOThHSUF5RG9ITlU1NkxWS2dlZHMrblJ1Q2NkOTlSYVNGaGhtcWR3aXRWeGtTekVUa2pPSzhhNHJ4YTVSYVNhQkRzczNTYkRKNWhpNjl3TDJmK1RVb3UwU1Y2WEt6aGNTU0ZLL214dlM2Y3YveE9wT1NnY2R1bDBXekN2VjZPVWc4UitQUHdwRlRTd3k4UFJOQ0NJa25iYWJzbFRDZy9tdDk2a3FMc2NLNjIxdkcrRUZsYmpZZTlld2c5dXVqVmxyVk05dldrRGVHTE1FS0pHbkVNclZtY25mYTNJVi8vRUxUQlJpUXFHWW1lOFQxTms0aWxsV2RvWk85MHd5clVrdGxWN1FINGVpbHFmdEpLNCtEZy95cUlSSnN4cmZtckNsYWZRaWtsRHNuZU1PWWJkWG5rbjBKVHVYMVovQ0JBUDQzL1R1T2tpRUwwMjIxQXI2NEowalU3QnR4OWpXWFhVL1NmblNDc2E4WmlSckV0cm9KVE9hMzkyTjdXYi9TS25YMDFYMGkzMG8zRkZzY3RHTmxDcGlETllNQUJrRm9HSktoaHdnVjRPb3F0Z3Y3RU83b0h2QkdDQXUzQTdTY29ua05YK3NoNGFDdE1WbnFzUkRxVmc1Q1QvVGdSL1lzZHVTb1U0Tk9nZG1QbTlxcFowVGpqNkdpV3V2L0dtbWpHQWQ0Z291NXJYZHg1QWh6d2ZSd1A2L2FZRHNEVUExWA"

if ambiance.startswith("😎"):
    st.sidebar.audio(
        trance_url,
        format="audio/mpeg",  # = mp3
        autoplay=True,
    )

    st.sidebar.markdown(
        """
    <div style='text-align: center; font-size: small; color: gray;'>
    © 2025 Laback feat. Alexis Carlier
    </div>
    """,
        unsafe_allow_html=True,
    )

elif ambiance.startswith("💿"):
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
        format="audio/mpeg",
        autoplay=True,
    )

    st.sidebar.markdown(
        """
    <div style='text-align: center; font-size: small; color: gray;'>
    © 1997 James Horner
    </div>
    """,
        unsafe_allow_html=True,
    )


st.sidebar.subheader("View all apps", divider=True)

st.sidebar.markdown(
    """
    <a href="https://share.streamlit.io/user/didierflamm" target="_blank">
        <img src="https://raw.githubusercontent.com/DidierFlamm/DidierFlamm/main/dids.webp" width="100%"; />
    </a>
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
        st.Page("pages/2_Visualisation.py", title="Visualisation", icon="📊"),
        st.Page("pages/3_Evaluation.py", title="Evaluation", icon="📝"),
        st.Page("pages/4_Optimisation.py", title="Optimisation", icon="📈"),
        st.Page("pages/5_Predictions.py", title="Predictions", icon="🎯"),
        st.Page("pages/6_Arrival.py", title="Port of arrival", icon="🏁"),
    ]

pg = st.navigation(st.session_state.pages, position="top")
pg.run()
