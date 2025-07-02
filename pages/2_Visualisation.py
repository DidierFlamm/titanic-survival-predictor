import streamlit as st
from utils import load_csv, to_display
import plotly.express as px


st.markdown(
    "<h2 style='text-align: center; color: #0366d6;'>📊 Visualisation</h2>",
    unsafe_allow_html=True,
)

df = load_csv(drop_outliers=False)
df_display = to_display(df)


st.subheader(":blue[Analyse univariée]", divider=True)

st.write(
    """
    L’analyse univariée consiste à examiner **chaque variable séparément**, sans tenir compte des autres. 
    Elle permet de comprendre la **répartition** des données, de détecter d’éventuels **déséquilibres**, 
    ou encore d’identifier des **outliers**, c'est à dire des valeurs extrêmes (statistiquement éloignées) ou aberrantes (souvent erronées).

    👉 Chaque onglet onglet ci-dessous présente une **visualisation unique** de la répartition de la **variable cible** (survie),
    ainsi que des **différentes caractéristiques** (âge, sexe, classe, tarif, etc.).

    Cette étape est essentielle pour avoir une première idée de la **structure des données** avant de passer 
    à des analyses plus complexes (bivariées ou multivariées) et enfin à la modélisation prédictive.
    """
)

(
    tab_survived,
    tab_sex,
    tab_age,
    tab_class,
    tab_fare,
    tab_sibsp,
    tab_parch,
    tab_embarked,
) = st.tabs(
    [
        "🛟 Survie",
        "♀️♂️ Sexe",
        "👶🧓 Age",
        "🎟️ Classe",
        "💰 Tarif",
        """🧑‍🤝‍🧑 Fratrie  
        & conjoint(e)""",
        """👨‍👩‍👦‍👦 Parents  
        & enfants""",
        "⚓ Embarquement",
    ]
)

with tab_survived:
    fig = px.pie(
        df_display,
        names="Survie",
        category_orders={"Survie": ["Oui", "Non"]},
        title="Répartition des survivants",
    )
    fig.update_traces(textposition="inside", textinfo="value+percent+label")
    st.plotly_chart(fig)

    st.write(
        """La variable cible indique si un passager a survécu (`Oui`) ou pas (`Non`).   
        On observe que moins de 39% des passages ont survécu."""
    )

with tab_sex:
    fig = px.pie(
        df_display,
        names="Sexe",
        category_orders={"Sexe": ["♀️ Femme", "♂️ Homme"]},
        title="Répartition des genres",
    )
    fig.update_traces(textposition="inside", textinfo="value+percent+label")
    st.plotly_chart(fig)
    st.write("Il y avait presque 2 fois plus d'hommes que de femmes à bord du Titanic")

with tab_age:
    fig = px.histogram(
        df_display, x="Age", title="Distribution des âges", marginal="box"
    )

    # Ajout du trait vertical pour la médiane
    median_age = df_display["Age"].median()
    fig.add_vline(
        x=median_age,
        line_dash="dash",
        line_color="red",
        annotation_text=f"{int(median_age)} ans",
        annotation_position="right",
    )
    st.plotly_chart(fig)
    st.write(
        """Les passagers du Titanic étaient âgés de 5 mois à 80 ans, avec une médiane à 28 ans. 50% des passagers ont entre 20 et 38 ans (intervalle interquartile). 
        Comme vu sur la page précédente, les âges de 177 passagers (soit 20%) ne sont pas renseignés dans le jeu de données. 
        La valeur médiane de la distribution (28 ans) leur sera arbitrairement attribuée."""
    )

with tab_class:
    fig = px.pie(
        df_display,
        names="Classe",
        category_orders={"Classe": ["1ère", "2ème", "3ème"]},
        title="Répartition des classes",
    )
    fig.update_traces(textposition="inside", textinfo="value+percent+label")
    st.plotly_chart(fig)
    st.write("La 3ème classe (populaire) est la plus représentée")

with tab_fare:
    fig = px.histogram(
        df_display, x="Tarif", title="Distribution des tarifs", marginal="box"
    )
    st.plotly_chart(fig)
    st.write(
        "Trois passagers présentent un tarif de £512.33, nettement supérieur à la distribution générale. Bien que ces valeurs extrêmes ne soient pas nécessairement aberrantes, elles sont considérées comme des outliers et seront exclues du jeu de données afin d'éviter qu’elles ne biaisent les résultats ultérieurs."
    )

with tab_sibsp:
    fig = px.pie(
        df_display,
        names="Fratrie & Conjoint(e)",
        category_orders={
            "Fratrie & Conjoint(e)": sorted(
                df_display["Fratrie & Conjoint(e)"].unique()
            )
        },
        title="""Répartition du nombre de frères, sœurs et conjoint(e)""",
    )
    fig.update_traces(
        textposition="inside",
        textinfo="value+percent+label",
        insidetextorientation="radial",
    )

    st.plotly_chart(fig)
    st.write("Plus de 2/3 des passagers voyagent sans frère ni sœur ni conjoint(e).")

with tab_parch:
    fig = px.pie(
        df_display,
        names="Parents & Enfants",
        category_orders={
            "Parents & Enfants": sorted(df_display["Parents & Enfants"].unique())
        },
        title="Répartition du nombre de parents et enfants",
    )
    fig.update_traces(
        textposition="inside",
        textinfo="value+percent+label",
        insidetextorientation="radial",
    )
    st.plotly_chart(fig)
    st.write("Plus de 3/4 des passagers voyagent sans parent ni enfant.")

with tab_embarked:
    fig = px.pie(
        df_display,
        names="Embarquement",
        title="Répartition des ports d'embarquement",
    )
    fig.update_traces(textposition="auto", textinfo="value+percent+label")
    st.plotly_chart(fig)
    st.write(
        """Près de 3/4 des passagers ont embarqués à Southampton (Angleterre).  
             Comme vu sur la page précédente, le port d'embarquement de 2 passagers n'est pas renseigné dans le jeu de données. 
             La valeur majoritaire ('Southampton') leur sera arbitrairement attribuée."""
    )


st.subheader(":blue[Analyse bivariée]", divider=True)

st.write(
    "L’analyse bivariée consiste à étudier la **relation entre deux variables** afin de comprendre comment elles interagissent ou sont liées. C’est une étape clé pour explorer un dataset avant de modéliser. "
)
st.write(
    "• L'analyse **target/feature** permet d’étudier comment une variable explicative (feature) est liée à la variable cible (target)."
)
st.write(
    "• L'analyse **feature/feature** permet d'explorer la relation entre 2 variables explicatives. Cela peut aider à détecter des dépendances, interactions, ou colinéarités qui influencent la modélisation."
)

df_display = df_display[df_display["Tarif"] < 500]
median_age = df_display["Age"].median()
embarked_mode = df_display["Embarquement"].mode()[0]
df_display["Age"] = df_display["Age"].fillna(median_age)
df_display["Embarquement"] = df_display["Embarquement"].fillna(embarked_mode)

(tab_sex_sur, tab_class_sur, tab_parch_sur, tab_embarked_sur, tab_embarked_class) = (
    st.tabs(
        [
            """🛟 Survie /  
            ♀️♂️ Sexe""",
            """🛟 Survie /  
            🎟️ Classe""",
            """🛟 Survie /  
            👨‍👩‍👦‍👦 Parents & enfants""",
            """🛟 Survie /  
            ⚓ Embarquement""",
            """🎟️ Classe /  
            ⚓ Embarquement""",
        ]
    )
)

with tab_sex_sur:

    fig = px.sunburst(
        df_display,
        path=["Sexe", "Survie"],
        title="Analyse de la survie en fonction du sexe des passagers",
    )
    st.plotly_chart(fig)

    st.write(
        """On constate que, proportionnellement, les femmes ont mieux survécu que les hommes :  
        • 232 survivantes sur 314 femmes, soit 74%  
        • 107 survivants sur 577 hommes, soit 19%"""
    )

with tab_class_sur:
    fig = px.sunburst(
        df_display,
        path=["Classe", "Survie"],
        title="Analyse de la survie en fonction de la classe",
    )
    st.plotly_chart(fig)

    st.write(
        """On constate que, proportionnellement, les passagers de 1ère classe ont mieux survécu que ceux de 2ème classe, qui ont mieux survécu que ceux de 3ème classe :  
        • 133 survivants sur 216 passagers en 1ère classe, soit 62%  
        • 87 survivants sur 184 passagers en 2ème classe, soit 47%
        • 119 survivants sur 491 passagers en 3ème classe, soit 24%"""
    )

with tab_parch_sur:
    fig = px.histogram(
        df_display,
        x="Parents & Enfants",
        color="Survie",
        barmode="stack",
        category_orders=dict(
            # Classe=["1ère", "2ème", "3ème"],
            Survie=["Oui", "Non"],
        ),
        title="Analyse de la survie en fonction du nombre de parents et enfants à bord du Titanic",
    )
    st.plotly_chart(fig)

    st.write(
        "On constate que, proportionnellement, les passagers voyageant avec parents et/ou enfants ont mieux survécu que ceux voyageant sans."
    )

with tab_embarked_sur:
    fig = px.sunburst(
        df_display,
        path=["Embarquement", "Survie"],
        title="Histogramme empilé de la survie en fonction du port d'embarquement",
    )

    st.plotly_chart(fig)
    st.write(
        """On constate que, proportionnellement, les passagers ayant embarqué à Cherbourg ont mieux survécu que les autres :  
            • 90 survivants sur 168 passagers ayant embarqué à Cherbourg (54%)  
            • 30 survivants sur 77 passagers ayant embarqué à Cherbourg (39%)  
            • 219 survivants sur 646 passagers ayant embarqué à Cherbourg (34%)"""
    )

with tab_embarked_class:
    fig = px.sunburst(
        df_display,
        path=["Embarquement", "Classe"],
        title="Analyse de la classe en fonction du port d'embarquement",
    )
    st.plotly_chart(fig)

    st.write(
        """On constate que les passagers ayant embarqué à Cherbourg ont majoritairement voyagé en 1ère classe alors que les passagers ayant embarqué à Queenstown ou Southampton ont voyagé très majoritairement en 3ème classe."""
    )
st.subheader(":blue[Analyse multivariée]", divider=True)

st.write(
    "L’analyse multivariée étudie simultanément les relations entre trois variables ou plus afin de mieux comprendre la structure complexe des données."
)
st.write(
    "Il existe de nombreuses méthodes d'analyse multivariée permettant de détecter les interactions, réduire la dimensionnalité ou encore segmenter les observations (ACP, AFC, clustering, etc...) mais nous n'aborderons ici que 2 visualisations multivariées par graphiques interactifs"
)
tab1, tab2 = st.tabs(
    ["♀️♂️ Sexe / 🛟 Survie / 🎟️ Classe", "⚓ Embarquement / 🛟 Survie / 🎟️ Classe"]
)

with tab1:
    fig = px.sunburst(
        df_display,
        path=["Sexe", "Survie", "Classe"],
        title="Tendances de survie par sexe et classe sur le Titanic",
    )
    st.plotly_chart(fig)

    st.write(
        """Ce graphique met en évidence 2 tendances:  
        • Les femmes n'ayant pas survécu voyageaient très majoritairement en 3ème classe (parmi les 81 femmes n'ayant pas survécu, 72 voyageaient en 3ème classe).  
        • Les hommes n'ayant pas survécu sont répartis sur les 3 classes mais un déséquilibre important est observée sur la classe 3 (parmi les 347 hommes voyageant en 3ème classe, 300 n'ont pas survécu)"""
    )

with tab2:
    fig = px.sunburst(
        df_display,
        path=["Embarquement", "Survie", "Classe"],
        title="Tendances de survie par port d'embarquement et classe sur le Titanic",
    )
    st.plotly_chart(fig)

    st.write(
        "On constate que la meilleure survie des passagers ayant embarqué à Cherbourg est corrélée à une plus grande proportion de passagers voyageant en 1ère classe que chez les passagers ayant embarqué à Queenstown ou Southampton"
    )

_, col, _ = st.columns(3)
with col:
    st.page_link(
        st.Page(
            "pages/3_Evaluation.py",
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
