import streamlit as st


st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>🏁 Port of arrival</h2>",
    unsafe_allow_html=True,
)


st.balloons()

# URL de la vidéo
video_url = "https://youtu.be/Sj9MEwjkxE0"

st.video(video_url, autoplay=True, muted=True)

st.subheader("🎉🚢")

st.write(
    """Au nom de tout l’équipage, je souhaite vous adresser mes plus sincères félicitations et remerciements pour avoir bravé avec succès cet océan de données. J’espère que ce projet vous a apporté autant de plaisir que d’apprentissage, et j’ai hâte de vous retrouver très bientôt pour de nouvelles aventures passionnantes avec la compagnie DIDS !
"""
)

st.markdown(
    """Vous pouvez consulter le code source de Titanic Survival Predictor sur <a href="https://github.com/DidierFlamm/titanic-survival-predictor" target="_blank">GitHub</a>, ainsi que découvrir toutes mes applications interactives sur <a href="https://share.streamlit.io/user/didierflamm" target="_blank">Streamlit Community Cloud</a>. N’hésitez pas à y faire un tour et à me faire part de vos retours par mail ✉️ [didier.flamm@gmail.com](mailto:didier.flamm@gmail.com) ou sur 🔗 [LinkedIn](https://www.linkedin.com/in/didier-flamm)""",
    unsafe_allow_html=True,
)

st.subheader(":blue[A bientôt !]")

st.divider()
st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
