# -*- coding: utf-8 -*-
import pandas as pd

from src.utils import rendement_du_trimestre


def calcul_retraite_tunisie(salaire_base: int, cout_trimestre: int) -> pd.DataFrame:
    """Calculate la retraite mensuelle pour un salarié du secteur public en Tunisie."""
    horizon_annees = 40
    trimestres = pd.Series(range(1, horizon_annees * 4 + 1), name="Trimestres")
    retraite = pd.DataFrame(
        columns=[
            "Periode cotisée (années)",
            "Valeur trimestre %",
            "Rendement total %",
            "Retraite mensuelle",
            "Rendement marginal",
            "Retour investissement trimestre %",
        ],
        index=trimestres,
    )

    retraite["Periode cotisée (années)"] = retraite.index / 4
    retraite["Valeur trimestre %"] = retraite.index.map(rendement_du_trimestre)
    retraite["Rendement total %"] = retraite["Valeur trimestre %"].cumsum().clip(upper=90)
    retraite["Retraite mensuelle"] = (retraite["Rendement total %"] / 100 * salaire_base).astype(int)
    retraite["Rendement marginal"] = (retraite["Valeur trimestre %"] / 100 * salaire_base).astype(int)
    retraite["Retour investissement trimestre %"] = retraite["Rendement marginal"] * 12 / cout_trimestre * 100

    return retraite.sort_index(ascending=False)
