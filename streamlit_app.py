# -*- coding: utf-8 -*-
import streamlit as st

import altair as alt


from src.calcul_retraite import calcul_retraite_tunisie, calcul_retraite_tunisie_styler
from src.investissement_vs_marche import simulation_rachat_vs_investissement
from src.sliders import (
    get_slider_salaire_base,
    get_slider_cout_rachat_trimestre,
    get_slider_nombre_annee_simulation,
    get_selecteur_affichage_calcul_retraite,
    get_slider_age_rachat_trimestres,
    get_slider_age_depart_retraite,
    get_slider_nombre_trimestres_rachetes,
    get_slider_nombre_annees_travaillees,
    get_slider_rendement_attendu_du_marche,
    get_slider_age_limite_simulation,
    get_checkbox_depenser_a_partir_de_la_retraite,
    get_checkbox_depenser_equiv_rachat_trimestres,
    get_toggle_afficher_valeurs_cumulees,
    get_comparison_y_labels,
    get_comparison_chart,
)
from src.utils import separator


st.set_page_config(
    page_title="Simulateur retraite personnel de Chedlia",
    page_icon=":earth_americas:",  # This is an emoji shortcode. Could be a URL too.
)
st.markdown(
    """
# :earth_africa: Simulateur retraite personnel de Chedlia

Simulateur de retraite et comparateur de rachat de trimestres versus investissement de capital.
""",
)

st.image("assets/background.jpeg", use_container_width=True)

st.header("Paramètres globaux", divider="gray")
salaire_base = get_slider_salaire_base()
cout_trimestre = get_slider_cout_rachat_trimestre()

separator(2)

st.header("Calcul montant retraite", divider="gray")

intervalle_annees = get_slider_nombre_annee_simulation()

separator()
retraite = calcul_retraite_tunisie(salaire_base, cout_trimestre)
retraite = retraite.loc[list(range(intervalle_annees[0] * 4, intervalle_annees[1] * 4 + 1))]


y_axis = get_selecteur_affichage_calcul_retraite()
y_max = retraite[y_axis].max() * 1.20

chart = (
    alt.Chart(retraite)
    .mark_line(point=True)
    .encode(
        x=alt.X(
            "Periode cotisée (années):Q",
            title="Periode cotisée (années)",
            axis=alt.Axis(format=".1f"),
        ),
        y=alt.Y(f"{y_axis}:Q", title=y_axis.capitalize(), scale=alt.Scale(domain=[0, y_max])),
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

separator()

st.dataframe(calcul_retraite_tunisie_styler(retraite))

separator(3)

st.header("Comparaison rachat trimestres vs investissement", divider="gray")

age_rachat_trimestres = get_slider_age_rachat_trimestres()
age_depart_retraite = get_slider_age_depart_retraite()
nombre_trimestres_rachetes = get_slider_nombre_trimestres_rachetes()
nombre_annees_travaillees = get_slider_nombre_annees_travaillees()
rendement_attendu_du_marche = get_slider_rendement_attendu_du_marche()
age_limite_simulation = get_slider_age_limite_simulation()
depenser_a_partir_de_la_retraite = get_checkbox_depenser_a_partir_de_la_retraite()
depenser_equiv_rachat_trimestres = get_checkbox_depenser_equiv_rachat_trimestres()


separator()

simulation_rachat_vs_marche = simulation_rachat_vs_investissement(
    age_rachat_trimestres,
    age_depart_retraite,
    nombre_trimestres_rachetes,
    nombre_annees_travaillees,
    salaire_base,
    cout_trimestre,
    rendement_attendu_du_marche,
    age_limite_simulation,
    depenser_a_partir_de_la_retraite,
    depenser_equiv_rachat_trimestres,
)

afficher_valeurs_cumulees = get_toggle_afficher_valeurs_cumulees()


y_columns, y_title = get_comparison_y_labels(afficher_valeurs_cumulees)

chart = get_comparison_chart(simulation_rachat_vs_marche, y_columns, y_title)

st.altair_chart(chart, use_container_width=True)

separator()

st.dataframe(simulation_rachat_vs_marche)

separator()
