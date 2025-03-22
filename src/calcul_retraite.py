# -*- coding: utf-8 -*-
import pandas as pd
from pandas.io.formats.style import Styler

from src.utils import rendement_du_trimestre


def calcul_retraite_tunisie(salaire_base: int, cout_trimestre: int) -> pd.DataFrame:
    """Calculate la retraite mensuelle pour un salarié du secteur public en Tunisie."""
    horizon_annees = 100
    trimestres = pd.Series(range(1, horizon_annees * 4 + 1), name="Trimestres")
    retraite = pd.DataFrame(
        columns=[
            "Periode cotisée (années)",
            "Valeur trimestre %",
            "Rendement total %",
            "Retraite mensuelle (DT)",
            "Rendement marginal mensuel (DT)",
            "Retour annuel rachat trimestre %",
        ],
        index=trimestres,
    )

    retraite["Periode cotisée (années)"] = retraite.index / 4
    retraite["Valeur trimestre %"] = retraite.index.map(rendement_du_trimestre)
    retraite["Rendement total %"] = retraite["Valeur trimestre %"].cumsum()
    retraite["Retraite mensuelle (DT)"] = (retraite["Rendement total %"] / 100 * salaire_base).round(1)
    retraite["Rendement marginal mensuel (DT)"] = (retraite["Valeur trimestre %"] / 100 * salaire_base).round(1)
    retraite["Retour annuel rachat trimestre %"] = (
        retraite["Rendement marginal mensuel (DT)"] * 12 / cout_trimestre * 100
    )
    return retraite.sort_index(ascending=False)


def calcul_retraite_tunisie_styler(retraite: pd.DataFrame) -> Styler:
    """Style la DataFrame de la retraite en Tunisie."""
    return retraite.style.format(
        {
            "Periode cotisée (années)": "{:.2f}",
            "Valeur trimestre %": "{:.2f}",
            "Rendement total %": "{:.2f}",
            "Retraite mensuelle (DT)": "{:.0f}",
            "Rendement marginal mensuel (DT)": "{:.1f}",
            "Retour annuel rachat trimestre %": "{:.2f}",
        },
    )
