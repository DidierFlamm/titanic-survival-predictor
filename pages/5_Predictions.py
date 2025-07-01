import streamlit as st
from utils import set_seed, load_csv, preprocess_data, get_fare_bounds, to_display
import pandas as pd

st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>🎯 Predictions</h2>",
    unsafe_allow_html=True,
)

if "df_results" not in st.session_state:
    st.info(
        """Les modèles doivent être optimisés avant de pouvoir réaliser des prédictions fiables.  
        Merci de bien vouloir exécuter l'étape 📈 Optimisation jusqu'à son terme.""",
        icon="ℹ️",
    )
    st.page_link(
        st.Page(
            "pages/4_Optimisation.py",
            title="📈 Optimisation",
            icon="👉",
        )
    )
    st.stop()

# URL de la vidéo
video_url = "https://youtu.be/vXBY6Zu46HE"

st.video(video_url, autoplay=True, muted=True)


set_seed()

st.write(
    "🛳️ Cher passager, merci pour votre patience ! La traversée des étapes d’évaluation et d’optimisation n’est pas toujours de tout repos – surtout quand les conditions algorithmiques sont capricieuses..."
)
st.write(
    """🌟 Nous voici enfin arrivés à destination : **les prédictions**, clou du spectacle et raison d’être de tout projet en intelligence artificielle.  
    Grâce aux modèles que nous avons précédemment optimisés, nous allons enfin pouvoir répondre à **la question qui nous guide depuis le début** :  
    _“Quels types de passagers avaient le plus de chances de survivre au naufrage du Titanic ?”_"""
)
st.write(
    """🧠 Pour y répondre, le modèle sélectionné va effectuer ce qu’on appelle une **prédiction** : il va estimer – à l’aide de méthodes statistiques apprises lors de l'entraînement – **la probabilité de survie individuelle** de chaque passager."""
)


st.subheader(
    (
        ":blue[Chances de survie des passagers]"
        if st.session_state.lang.startswith("fr")
        else ":blue[Survival chances of passengers]"
    ),
    divider=True,
)

st.write(
    """🔍 Commençons par calculer les **probabilités de survie** des passagers qui étaient à bord du Titanic.  
    Nous allons ensuite les **classer par ordre décroissant** de chance de survie, afin d’identifier ceux qui avaient le plus – ou le moins – de chances de s’en sortir selon notre modèle."""
)

model_choisi = st.selectbox(
    label=(
        "Choisir le modèle"
        if st.session_state.lang.startswith("fr")
        else "Choose the model"
    ),
    options=list(st.session_state.df_results.Model),
)

if model_choisi is None:
    st.error("Aucun modèle à choisir")
    st.stop()
else:
    model = st.session_state[model_choisi]

st.write(
    f"📌 balanced accuracy of {model_choisi} model = **{st.session_state.df_results.loc[st.session_state.df_results.Model == model_choisi, "Balanced Accuracy"
].values[0]} %**"
)

set_seed()
df = load_csv(drop_outliers=True)
X, _, y, _ = preprocess_data(df, split=False)


y_proba = model.predict_proba(X)
y_pred = model.predict(X)

df_display = to_display(df)

df_display.insert(
    loc=0, column="Chance de survie", value=(y_proba[:, 1] * 100).round(2)
)
df_display = df_display.sort_values(by="Chance de survie", ascending=False)
df_display.insert(
    loc=2,
    column="Prédiction correcte ?",
    value=y_pred == y,
)
df_display["Prédiction correcte ?"] = df_display["Prédiction correcte ?"].apply(
    lambda x: "✔️" if x else "❌"
)

st.dataframe(df_display)

st.caption(f"seed de la session = {st.session_state.seed}")


st.write(
    "Les chances de survie des passagers sont prédites par un modèle optimisé, avec :"
    if st.session_state.lang.startswith("fr")
    else "The chances of survival are predicted by an optimized model, with :"
)

st.write(
    """• chance de survie ≥ 50% : le modèle prédit que le passager survit  
• chance de survie < 50% : le modèle prédit que le passager ne survit pas si sa """
    if st.session_state.lang.startswith("fr")
    else """• probability ≥ 50%: the passenger survives  
• probability < 50%: the passenger does not survive"""
)

st.write(
    """La prédiction est qualifiée de correcte ✔️ si la prédiction de survie du passager est conforme à la réalité. Sinon, la prédiction est incorrecte ❌."""
)

counts = df_display["Prédiction correcte ?"].value_counts()
frequencies = df_display["Prédiction correcte ?"].value_counts(normalize=True)
result = pd.DataFrame(
    {"Nb": counts, "%": (100 * frequencies).round(2).astype(str) + " %"}
)

st.dataframe(result)

st.subheader(
    (
        ":blue[Chance de survie d'un passager personnalisé]"
        if st.session_state.lang.startswith("fr")
        else ":blue[Survival chance of a custom passenger]"
    ),
    divider=True,
)

st.write(
    """🧐 **Interpréter une prédiction** n’est pas toujours évident.  
    Pour répondre pleinement à notre question initiale, il ne suffit pas de savoir *qui* a survécu : il faut aussi comprendre **pourquoi** certains passagers avaient plus de chances que d’autres.  

Certains modèles sont dits **interprétables** (comme les arbres de décision ou les k-neighbors), car leur logique peut être représentée visuellement. D'autres en revanche, comme les forêts aléatoires ou les réseaux de neurones, sont de véritables **boîtes noires**, dont les mécanismes internes restent difficiles à décoder."""
)

st.write(
    """Une méthode simple et universelle consiste à **jouer avec un exemple** : on sélectionne un passager aléatoire, on observe sa probabilité de survie, puis on modifie ses caractéristiques (âge, sexe, classe…) pour voir comment cela influence la prédiction.  
    👉 **À vous de jouer !** Remplissez le formulaire ci-dessous et observez l’impact de chaque paramètre sur la chance de survie."""
)

st.write(
    """⚠️ **Âmes sensibles s’abstenir !** Si vous n’avez pas le mal de mer, vous pouvez même tester *votre propre chance de survie* – autrement dit, celle qu’aurait eue un passager avec vos caractéristiques.  
    La compagnie **DIDS** décline toute responsabilité en cas de prédiction peu rassurante... 🛟"""
)

col1, col2 = st.columns(2, border=True)

bounds = get_fare_bounds(df)

with col1:

    st.markdown(
        """<div style="text-align: center;"><em>Caractéristiques du passager</em></div>""",
        unsafe_allow_html=True,
    )
    st.write("")

    st.radio(
        "**Sexe**",
        ("female", "male"),
        format_func=lambda x: "Femme" if x == "female" else "Homme",
        horizontal=True,
        key="sexe",
    )

    st.slider("**Age**", 0, 100, 50, key="age")

    st.radio("**Classe**", (1, 2, 3), index=1, horizontal=True, key="pclass")

    st.slider(
        "**Tarif**",
        int(bounds[st.session_state.pclass]["min"]),
        int(bounds[st.session_state.pclass]["max"]),
        int(bounds[st.session_state.pclass]["median"]),
        key="fare",
    )

    st.caption("tarif par défaut = valeur médiane de la classe")

    st.selectbox(
        "**Port d'embarquement**",
        options=["C", "Q", "S"],
        index=0,
        format_func=lambda x: {
            "C": "🇫🇷 Cherbourg",
            "Q": "🇮🇪 Queenstown",
            "S": "🇬🇧 Southampton",
        }[x],
        key="embarked",
    )


with col2:
    st.markdown(
        """<div style="text-align: center;"><em>Famille du passager (à bord du Titanic)</em></div>""",
        unsafe_allow_html=True,
    )
    st.write("")

    st.radio(
        "**Époux(se)**",
        [1, 0],
        index=1,
        format_func=lambda x: "Oui" if x else "Non",
        horizontal=True,
        key="spouse",
    )

    st.slider("**Frères et sœurs**", 0, 10, 0, key="siblings")

    st.radio("**Parents**", (0, 1, 2), horizontal=True, key="parents")

    st.slider("**Enfants**", 0, 10, 0, key="children")

custom = pd.DataFrame(
    [
        [
            st.session_state.pclass,
            st.session_state.sexe,
            st.session_state.age,
            st.session_state.spouse + st.session_state.siblings,
            st.session_state.parents + st.session_state.children,
            st.session_state.fare,
            st.session_state.embarked,
        ]
    ],
    columns=["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"],
)
custom.index = pd.Index(["Passenger"])


set_seed()
# st.write(st.session_state.columns)
X, _, _, _ = preprocess_data(custom, split=False)
X = X.reindex(columns=st.session_state["columns"], fill_value=0)
# st.dataframe(X)
model = st.session_state[model_choisi]
y_prob = model.predict_proba(X)

chance = round(100 * y_prob[0, 1])

st.metric(
    "Survival chance predicted",
    ("🟢" if chance >= 50 else "🔴") + f" {chance} %",
)

custom.columns = [
    "Classe",
    "Sexe",
    "Age",
    "Fratrie & Conjoint(e)",
    "Parents & Enfants",
    "Tarif",
    "Embarquement",
]

st.dataframe(custom)

_, col, _ = st.columns(3)
with col:
    st.write("")
    st.write("")
    st.page_link(
        st.Page(
            "pages/6_Arrival.py",
            title=(
                "Passer à l'étape suivante"
                if st.session_state.lang.startswith("fr")
                else "Go to the next step"
            ),
            icon="➡️",
        )
    )

st.divider()

st.markdown(
    """
    <div style='text-align: center; font-size: small; color: gray;'>
    © 2025 Didier Flamm
    </div>
    """,
    unsafe_allow_html=True,
)
