# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import altair as alt

from src import constants, settings


def get_slider_salaire_base() -> int:
    """Get the base salary slider."""
    return st.slider(
        "Quel est le salaire de base net estimé au moment de la retraite? (prendre la moyenne des 3 dernières années)",
        min_value=constants.global_params.salaire_base.min_,
        max_value=constants.global_params.salaire_base.max_,
        value=settings.global_params.salaire_base,
        step=constants.global_params.salaire_base.step,
    )


def get_slider_cout_rachat_trimestre() -> int:
    """Get the trimester buyback cost slider."""
    return st.slider(
        "Quel est le coût de rachat du trimestre?",
        min_value=constants.global_params.cout_rachat_trimestre.min_,
        max_value=constants.global_params.cout_rachat_trimestre.max_,
        value=settings.global_params.cout_trimestre,
        step=constants.global_params.cout_rachat_trimestre.step,
    )


def get_slider_nombre_annees_simulation() -> tuple[int, int]:
    """Get the simulation year range slider."""
    return st.slider(
        "Nombre d'années pour la simulation?",
        min_value=constants.calcul_montant_retraite.nombre_annees_simulation.min_,
        max_value=constants.calcul_montant_retraite.nombre_annees_simulation.max_,
        value=settings.calcul_montant_retraite.nombre_annees_simulation,
        step=constants.calcul_montant_retraite.nombre_annees_simulation.step,
    )


def get_selecteur_affichage_calcul_retraite() -> str:
    """Get the retirement calculation display selector."""
    return st.selectbox(
        "Valeur à afficher:",
        options=constants.calcul_montant_retraite.affichage_calcul_retraite.options,
        index=settings.calcul_montant_retraite.affichage_calcul_retraite,
    )


def get_slider_age_rachat_trimestres() -> int:
    """Get the trimester buyback age slider."""
    return st.slider(
        "A quel âge souhaitez-vous racheter des trimestres?",
        min_value=constants.comparaison_rachat_vs_investissement.age_rachat_trimestres.min_,
        max_value=constants.comparaison_rachat_vs_investissement.age_rachat_trimestres.max_,
        value=settings.comparaison_rachat_vs_investissement.age_rachat_trimestres,
        step=constants.comparaison_rachat_vs_investissement.age_rachat_trimestres.step,
    )


def get_slider_age_depart_retraite() -> int:
    """Get the retirement age slider."""
    return st.slider(
        "A quel âge souhaitez-vous prendre votre retraite?",
        min_value=constants.comparaison_rachat_vs_investissement.age_depart_retraite.min_,
        max_value=constants.comparaison_rachat_vs_investissement.age_depart_retraite.max_,
        value=settings.comparaison_rachat_vs_investissement.age_depart_retraite,
        step=constants.comparaison_rachat_vs_investissement.age_depart_retraite.step,
    )


def get_slider_nombre_trimestres_rachetes() -> int:
    """Get the trimester buyback slider."""
    return st.slider(
        "Combien de trimestres souhaitez-vous racheter?",
        min_value=constants.comparaison_rachat_vs_investissement.nombre_trimestres_rachetes.min_,
        max_value=constants.comparaison_rachat_vs_investissement.nombre_trimestres_rachetes.max_,
        value=settings.comparaison_rachat_vs_investissement.nombre_trimestres_rachetes,
        step=constants.comparaison_rachat_vs_investissement.nombre_trimestres_rachetes.step,
    )


def get_slider_nombre_annees_travaillees() -> int:
    """Get the number of years worked slider."""
    return st.slider(
        "Combien d'années auriez-vous cotisé au moment de la retraite, hors rachat de trimestres?",
        min_value=constants.comparaison_rachat_vs_investissement.nombre_annees_travaillees.min_,
        max_value=constants.comparaison_rachat_vs_investissement.nombre_annees_travaillees.max_,
        value=settings.comparaison_rachat_vs_investissement.nombre_annees_travaillees,
        step=constants.comparaison_rachat_vs_investissement.nombre_annees_travaillees.step,
    )


def get_slider_rendement_attendu_du_marche() -> float:
    """Get the expected market return slider."""
    return st.slider(
        "Quel rendement annuel attendez-vous d'un investissement au marché en %?",
        min_value=constants.comparaison_rachat_vs_investissement.rendement_attendu_du_marche.min_,
        max_value=constants.comparaison_rachat_vs_investissement.rendement_attendu_du_marche.max_,
        value=settings.comparaison_rachat_vs_investissement.rendement_attendu_du_marche,
        step=constants.comparaison_rachat_vs_investissement.rendement_attendu_du_marche.step,
    )


def get_slider_age_limite_simulation() -> int:
    """Get the simulation age limit slider."""
    return st.slider(
        "Jusqu'à quel âge souhaitez-vous simuler?",
        min_value=constants.comparaison_rachat_vs_investissement.age_limite_simulation.min_,
        max_value=constants.comparaison_rachat_vs_investissement.age_limite_simulation.max_,
        value=settings.comparaison_rachat_vs_investissement.age_limite_simulation,
        step=constants.comparaison_rachat_vs_investissement.age_limite_simulation.step,
    )


def get_checkbox_depenser_a_partir_de_la_retraite() -> bool:
    """Get the retirement spending checkbox."""
    return st.checkbox(
        "Comptez-vous attendre la retraite pour commencer à dépenser la rente de votre investissement?",
        value=settings.comparaison_rachat_vs_investissement.depenser_a_partir_de_la_retraite,
    )


def get_checkbox_depenser_equiv_rachat_trimestres() -> bool:
    """Get the equivalent trimester buyback spending checkbox."""
    return st.checkbox(
        "Souhaitez-vous dépenser l'équivalent de la rente du rachat de trimestres et épargner le reste du retour de votre investissement?",
        value=settings.comparaison_rachat_vs_investissement.depenser_equiv_rachat_trimestre,
    )


def get_toggle_afficher_valeurs_cumulees() -> bool:
    """Get the cumulative values toggle."""
    return st.checkbox(
        "Afficher les valeurs cumulées",
        value=settings.comparaison_rachat_vs_investissement.afficher_valeurs_cumulees,
    )


def get_comparison_y_labels(afficher_valeurs_cumulees: bool) -> tuple[list[str], str]:
    """Get the comparison chart y labels."""
    if not afficher_valeurs_cumulees:
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
    return y_columns, y_title


def get_comparison_chart(simulation_rachat_vs_marche: pd.DataFrame, y_columns: list[str], y_title: str) -> alt.Chart:
    """Get the comparison chart."""
    return (
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
