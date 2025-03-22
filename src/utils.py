# -*- coding: utf-8 -*-
import streamlit as st


def get_rente_annuelle_rachat_trimestres(
    nombre_trimestres_rachetes: int,
    nombre_annees_travaillees: int,
    salaire_base: int,
) -> int:
    """Calculate la rente annuelle pour un rachat de trimestres."""
    rente_mensuelle = (
        nombre_trimestres_rachetes * rendement_du_trimestre(nombre_annees_travaillees * 4) / 100 * salaire_base
    )
    return int(rente_mensuelle * 12)


def rendement_du_trimestre(trimestre: int) -> float:
    """Calculate le rendement d'un trimestre."""
    if trimestre <= 40:
        return 0.5
    if trimestre <= 80:
        return 0.75
    if trimestre <= 160:
        return 0.5
    return 0


def separator(count: int = 1) -> None:
    """Print a separator."""
    for _ in range(count):
        st.write("")
