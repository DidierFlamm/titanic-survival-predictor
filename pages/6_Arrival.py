import streamlit as st
from utils import stream_data

st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>🏁 Port of arrival</h2>",
    unsafe_allow_html=True,
)


st.balloons()

# URL de la vidéo
video_url = "https://youtu.be/Sj9MEwjkxE0"

st.video(video_url, autoplay=True, muted=True)

st.subheader("🎉🚢")

st.write_stream(
    stream_data(
        """Au nom de tous les membres de l’équipage, je souhaite vous adresser mes plus sincères **félicitations** et **remerciements** pour avoir bravé avec succès cet océan de données. J’espère que ce projet vous a apporté autant de plaisir que d’apprentissage, et j’ai hâte de vous retrouver très bientôt pour de nouvelles expériences passionnantes avec la compagnie **DIDS** !
"""
    )
)


st.subheader(":blue[A bientôt 🫡]")

st.write("**Didier**")

st.divider()

st.markdown(
    """_Le code source du projet Titanic Survival Predictor est disponible sur <a href="https://github.com/DidierFlamm/titanic-survival-predictor" target="_blank">GitHub</a>.  
    Découvrez toutes mes applications interactives sur <a href="https://share.streamlit.io/user/didierflamm" target="_blank">Streamlit Community Cloud</a>. N’hésitez pas à y faire un tour puis me faire part de vos impressions via ✉️ [didier.flamm@gmail.com](mailto:didier.flamm@gmail.com) ou [LinkedIn](https://www.linkedin.com/in/didier-flamm)._""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
