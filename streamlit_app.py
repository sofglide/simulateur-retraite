# -*- coding: utf-8 -*-
import streamlit as st

import altair as alt


from src.calcul_retraite import calcul_retraite_tunisie
from src.investissement_vs_marche import simulation_rachat_vs_investissement

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Simulateur retraite",
    page_icon=":earth_americas:",  # This is an emoji shortcode. Could be a URL too.
)
st.markdown(
    """
# :earth_africa: Simulateur retraite

Simulateur de retraite et comparateur de rachat de trimestres versus investissement de capital.
""",
)

st.write("")
st.write("")

st.header("Calcul montant retraite", divider="gray")

salaire_base_min = 1000
salaire_base_max = 5000
salaire_base_default = 3000
salaire_base = st.slider(
    "Quel est le salaire de base net estimé au moment de la retraite? (prendre la moyenne des 3 dernières années)",
    min_value=salaire_base_min,
    max_value=salaire_base_max,
    value=salaire_base_default // 2,
    step=100,
)

cout_trimestre_base_min = 500
cout_trimestre_base_max = 5000
cout_trimestre_default = 2500
cout_trimestre = st.slider(
    "Quel est le coût de rachat du trimestre?",
    min_value=cout_trimestre_base_min,
    max_value=cout_trimestre_base_max,
    value=cout_trimestre_default // 2,
    step=100,
)

trimestres_min = 1
trimestres_max = 160
trimestres_default = [25 * 4, 35 * 4]
intervalle_trimestres = st.slider(
    "Nombre de trimestres pour la simulation?",
    min_value=trimestres_min,
    max_value=trimestres_max,
    value=trimestres_default,
    step=1,
)

st.write("")
retraite = calcul_retraite_tunisie(salaire_base, cout_trimestre)
retraite = retraite.loc[list(range(intervalle_trimestres[0], intervalle_trimestres[1] + 1))]


y_axis = st.selectbox(
    "Valeur à afficher:",
    options=[
        "Valeur trimestre %",
        "Rendement total %",
        "Retraite mensuelle",
    ],
    index=2,
)
y_max = retraite[y_axis].max() * 1.20

chart = (
    alt.Chart(retraite)
    .mark_line(point=True)
    .encode(
        x=alt.X("Periode cotisée (années):O", title="Periode cotisée (années)"),
        y=alt.Y(f"{y_axis}:Q", title=y_axis.capitalize(), scale=alt.Scale(domain=[0, y_max])),
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

st.write("")

st.dataframe(retraite)

st.write("")
st.write("")
st.write("")

st.header("Comparaison rachat trimestres vs investissement", divider="gray")

age_rachat_trimestres_sim = st.slider(
    "A quel âge souhaitez-vous racheter des trimestres?",
    min_value=50,
    max_value=65,
    value=55,
    step=1,
    key="sim_age_rachat_trimestres",
)

age_depart_retraite_sim = st.slider(
    "A quel âge souhaitez-vous prendre votre retraite?",
    min_value=60,
    max_value=70,
    value=65,
    step=1,
    key="sim_age_depart_retraite",
)

nombre_trimestres_rachetes_sim = st.slider(
    "Combien de trimestres souhaitez-vous racheter?",
    min_value=1,
    max_value=20,
    value=12,
    step=1,
    key="sim_trimestres_rachetes",
)

nombre_annees_travaillees_sim = st.slider(
    "Combien d'années auriez-vous cotisé au moment de la retraite, hors rachat de trimestres?",
    min_value=25,
    max_value=40,
    value=35,
    step=1,
    key="sim_annees_travaillees",
)

rendement_attendu_du_marche_sim = st.slider(
    "Quel rendement annuel attendez-vous d'un investissement au marché en %?",
    min_value=0.0,
    max_value=30.0,
    value=5.0,
    step=0.1,
    key="sim_rendement_marche",
)

age_limite_simulation_sim = st.slider(
    "Jusqu'à quel âge souhaitez-vous simuler?",
    min_value=70,
    max_value=100,
    value=80,
    step=1,
    key="sim_age_limite",
)

salaire_base_min = 1000
salaire_base_max = 5000
salaire_base_default = 3000
salaire_base_sim = st.slider(
    "Quel est le salaire de base net estimé au moment de la retraite? (prendre la moyenne des 3 dernières années)",
    min_value=salaire_base_min,
    max_value=salaire_base_max,
    value=salaire_base_default,
    step=100,
    key="sim_salaire_base",
)

cout_trimestre_base_min = 500
cout_trimestre_base_max = 5000
cout_trimestre_default = 2500
cout_trimestre_sim = st.slider(
    "Quel est le coût de rachat du trimestre?",
    min_value=cout_trimestre_base_min,
    max_value=cout_trimestre_base_max,
    value=cout_trimestre_default // 2,
    step=100,
    key="sim_cout_trimestre",
)

depenser_a_partir_de_la_retraite_sim = st.checkbox(
    "Comptez-vous attendre la retraite pour commencer à dépenser la rente de votre investissement?",
    value=True,
    key="sim_depenser_retraite",
)

depenser_equiv_rachat_trimestres_sim = st.checkbox(
    "Souhaitez-vous dépenser l'équivalent de la rente du rachat de trimestres et épargner le reste du retour de votre investissement?",
    value=False,
    key="sim_depenser_tout",
)

st.write("")

simulation_rachat_vs_marche = simulation_rachat_vs_investissement(
    age_rachat_trimestres_sim,
    age_depart_retraite_sim,
    nombre_trimestres_rachetes_sim,
    nombre_annees_travaillees_sim,
    salaire_base_sim,
    cout_trimestre_sim,
    rendement_attendu_du_marche_sim,
    age_limite_simulation_sim,
    depenser_a_partir_de_la_retraite_sim,
    depenser_equiv_rachat_trimestres_sim,
)

afficher_valeurs_cumulees_sim = st.toggle("Afficher les valeurs cumulées", value=True, key="sim_valeurs_cumulees")

if not afficher_valeurs_cumulees_sim:
    y_columns = [
        "Rente annuelle rachat trimestres",
        "Rente annuelle marché",
        "Surplus capital",
    ]
    y_title = "Valeurs annuelles"
else:
    y_columns = [
        "Rente annuelle cumulée rachat trimestres",
        "Rente annuelle cumulée marché",
        "Surplus capital cumulé",
    ]
    y_title = "Valeurs annuelles cumulées"

chart = (
    alt.Chart(simulation_rachat_vs_marche.reset_index())
    .transform_fold(
        y_columns,
        as_=["variable", "value"],
    )
    .mark_line(point=True)
    .encode(
        x=alt.X("Âge:O", title="Âge"),
        y=alt.Y("value:Q", title=y_title),
        color=alt.Color(
            "variable:N",
            title="Metric",
            legend=alt.Legend(
                labelLimit=0,  # disable truncation
                labelFontSize=10,
                orient="right",
            ),
        ),
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

st.write("")

st.dataframe(simulation_rachat_vs_marche)

st.write("")
