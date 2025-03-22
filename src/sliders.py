# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import altair as alt


def get_slider_salaire_base(
    salaire_base_min: int = 1000,
    salaire_base_max: int = 5000,
    salaire_base_default: int = 3000,
) -> int:
    """Get the base salary slider."""
    return st.slider(
        "Quel est le salaire de base net estimé au moment de la retraite? (prendre la moyenne des 3 dernières années)",
        min_value=salaire_base_min,
        max_value=salaire_base_max,
        value=salaire_base_default // 2,
        step=100,
    )


def get_slider_cout_rachat_trimestre(
    cout_trimestre_base_min: int = 500,
    cout_trimestre_base_max: int = 5000,
    cout_trimestre_default: int = 2500,
) -> int:
    """Get the trimester buyback cost slider."""
    return st.slider(
        "Quel est le coût de rachat du trimestre?",
        min_value=cout_trimestre_base_min,
        max_value=cout_trimestre_base_max,
        value=cout_trimestre_default // 2,
        step=100,
    )


def get_slider_nombre_annee_simulation(
    nombre_annees_simulation_min: int = 1,
    nombre_annees_simulation_max: int = 50,
    nombre_annees_simulation_default: tuple[int, int] = (25, 35),
) -> tuple[int, int]:
    """Get the simulation year range slider."""
    return st.slider(
        "Nombre d'années pour la simulation?",
        min_value=nombre_annees_simulation_min,
        max_value=nombre_annees_simulation_max,
        value=nombre_annees_simulation_default,
        step=1,
    )


def get_selecteur_affichage_calcul_retraite() -> str:
    """Get the retirement calculation display selector."""
    return st.selectbox(
        "Valeur à afficher:",
        options=[
            "Valeur trimestre %",
            "Rendement total %",
            "Retraite mensuelle (DT)",
        ],
        index=2,
    )


def get_slider_age_rachat_trimestres(
    age_rachat_trimestres_min: int = 50,
    age_rachat_trimestres_max: int = 65,
    age_rachat_trimestres_default: int = 55,
) -> int:
    """Get the trimester buyback age slider."""
    return st.slider(
        "A quel âge souhaitez-vous racheter des trimestres?",
        min_value=age_rachat_trimestres_min,
        max_value=age_rachat_trimestres_max,
        value=age_rachat_trimestres_default,
        step=1,
    )


def get_slider_age_depart_retraite(
    age_depart_retraite_min: int = 60,
    age_depart_retraite_max: int = 70,
    age_depart_retraite_default: int = 65,
) -> int:
    """Get the retirement age slider."""
    return st.slider(
        "A quel âge souhaitez-vous prendre votre retraite?",
        min_value=age_depart_retraite_min,
        max_value=age_depart_retraite_max,
        value=age_depart_retraite_default,
        step=1,
    )


def get_slider_nombre_trimestres_rachetes(
    nombre_trimestres_rachetes_min: int = 1,
    nombre_trimestres_rachetes_max: int = 20,
    nombre_trimestres_rachetes_default: int = 12,
) -> int:
    """Get the trimester buyback slider."""
    return st.slider(
        "Combien de trimestres souhaitez-vous racheter?",
        min_value=nombre_trimestres_rachetes_min,
        max_value=nombre_trimestres_rachetes_max,
        value=nombre_trimestres_rachetes_default,
        step=1,
    )


def get_slider_nombre_annees_travaillees(
    nombre_annees_travaillees_min: int = 25,
    nombre_annees_travaillees_max: int = 40,
    nombre_annees_travaillees_default: int = 35,
) -> int:
    """Get the number of years worked slider."""
    return st.slider(
        "Combien d'années auriez-vous cotisé au moment de la retraite, hors rachat de trimestres?",
        min_value=nombre_annees_travaillees_min,
        max_value=nombre_annees_travaillees_max,
        value=nombre_annees_travaillees_default,
        step=1,
    )


def get_slider_rendement_attendu_du_marche(
    rendement_attendu_du_marche_min: float = 0.0,
    rendement_attendu_du_marche_max: float = 30.0,
    rendement_attendu_du_marche_default: float = 5.0,
) -> float:
    """Get the expected market return slider."""
    return st.slider(
        "Quel rendement annuel attendez-vous d'un investissement au marché en %?",
        min_value=rendement_attendu_du_marche_min,
        max_value=rendement_attendu_du_marche_max,
        value=rendement_attendu_du_marche_default,
        step=0.1,
    )


def get_slider_age_limite_simulation(
    age_limite_simulation_min: int = 70,
    age_limite_simulation_max: int = 100,
    age_limite_simulation_default: int = 80,
) -> int:
    """Get the simulation age limit slider."""
    return st.slider(
        "Jusqu'à quel âge souhaitez-vous simuler?",
        min_value=age_limite_simulation_min,
        max_value=age_limite_simulation_max,
        value=age_limite_simulation_default,
        step=1,
    )


def get_checkbox_depenser_a_partir_de_la_retraite() -> bool:
    """Get the retirement spending checkbox."""
    return st.checkbox(
        "Comptez-vous attendre la retraite pour commencer à dépenser la rente de votre investissement?",
        value=True,
    )


def get_checkbox_depenser_equiv_rachat_trimestres() -> bool:
    """Get the equivalent trimester buyback spending checkbox."""
    return st.checkbox(
        "Souhaitez-vous dépenser l'équivalent de la rente du rachat de trimestres et épargner le reste du retour de votre investissement?",
        value=False,
    )


def get_toggle_afficher_valeurs_cumulees() -> bool:
    """Get the cumulative values toggle."""
    return st.checkbox("Afficher les valeurs cumulées", value=True)


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
