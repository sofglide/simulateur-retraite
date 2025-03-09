# -*- coding: utf-8 -*-
import pandas as pd
import math

from src.utils import get_rente_annuelle_rachat_trimestres


def simulation_rachat_vs_investissement(
    age_rachat_trimestres: int,
    age_depart_retraite: int,
    nombre_trimestres_rachetes: int,
    nombre_annees_travaillees: int,
    salaire_base: int,
    cout_trimestre: int,
    rendement_marche: float,
    age_limite_simulation: int,
    depenser_a_partir_de_la_retraite: bool,
    ne_pas_depenser_plus_que_rendement_retraite: bool,
) -> pd.DataFrame:
    """Simulate la rente annuelle et cumulée d'un rachat de trimestres par rapport à un investissement en bourse."""
    rente_retraite = _rente_annuelle_rachat_trimestres(
        age_rachat_trimestres,
        age_depart_retraite,
        nombre_trimestres_rachetes,
        nombre_annees_travaillees,
        salaire_base,
        age_limite_simulation,
    )
    rente_cumulee_retraite = _rente_cumulee_rachat_trimestres(
        age_rachat_trimestres,
        age_depart_retraite,
        nombre_trimestres_rachetes,
        nombre_annees_travaillees,
        salaire_base,
        age_limite_simulation,
    )
    montant_rente_annuelle_rachat_trimestres = get_rente_annuelle_rachat_trimestres(
        nombre_trimestres_rachetes,
        nombre_annees_travaillees,
        salaire_base,
    )
    rente_marche = _rente_annuelle_marche(
        cout_trimestre * nombre_trimestres_rachetes,
        rendement_marche,
        age_rachat_trimestres,
        age_depart_retraite,
        age_limite_simulation,
        depenser_a_partir_de_la_retraite,
        montant_rente_annuelle_rachat_trimestres,
        ne_pas_depenser_plus_que_rendement_retraite,
    )
    rente_cumulee_marche = _rente_annuelle_cumulee_marche(
        cout_trimestre * nombre_trimestres_rachetes,
        rendement_marche,
        age_rachat_trimestres,
        age_depart_retraite,
        age_limite_simulation,
        depenser_a_partir_de_la_retraite,
        montant_rente_annuelle_rachat_trimestres,
        ne_pas_depenser_plus_que_rendement_retraite,
    )
    sim = pd.concat(
        [rente_retraite, rente_marche, rente_cumulee_retraite, rente_cumulee_marche],
        axis=1,
    )
    sim.index.name = "Âge"
    return sim


def _rente_annuelle_rachat_trimestres(
    age_rachat_trimestres: int,
    age_depart_retraite: int,
    nombre_trimestres_rachetes: int,
    nombre_annees_travaillees: int,
    salaire_base: int,
    age_limite_simulation: int,
) -> pd.Series:
    rente_annuelle = get_rente_annuelle_rachat_trimestres(
        nombre_trimestres_rachetes,
        nombre_annees_travaillees,
        salaire_base,
    )
    rente_percue = [0 for _ in range(age_rachat_trimestres, age_depart_retraite + 1)] + [
        rente_annuelle for _ in range(age_depart_retraite + 1, age_limite_simulation + 1)
    ]
    return pd.Series(
        index=list(range(age_rachat_trimestres, age_limite_simulation + 1)),
        data=rente_percue,
        name="Rente annuelle rachat trimestres",
    ).astype(int)


def _rente_cumulee_rachat_trimestres(
    age_rachat_trimestres: int,
    age_depart_retraite: int,
    nombre_trimestres_rachetes: int,
    nombre_annees_travaillees: int,
    salaire_base: int,
    age_limite_simulation: int,
) -> pd.Series:
    rente_annuelle = _rente_annuelle_rachat_trimestres(
        age_rachat_trimestres,
        age_depart_retraite,
        nombre_trimestres_rachetes,
        nombre_annees_travaillees,
        salaire_base,
        age_limite_simulation,
    )
    return rente_annuelle.cumsum().rename("Rente annuelle cumulée rachat trimestres")


def _rente_annuelle_marche(
    capital_investi: int,
    rendement_marche: float,
    age_investissement: int,
    age_depart_retraite: int,
    age_limite_simulation: int,
    depenser_a_partir_de_la_retraite: bool,
    rente_annuelle_rachat_trimestres: int,
    ne_pas_depenser_plus_que_rendement_retraite: bool,
) -> pd.DataFrame:
    rendement_mensuel = math.exp(math.log(1 + rendement_marche / 100) / 12) - 1
    capital: float = capital_investi
    rente_annuelle: list[float] = []
    capital_ajoute: list[float] = []
    for age in range(age_investissement, age_limite_simulation + 1):
        if depenser_a_partir_de_la_retraite and age <= age_depart_retraite:
            rente_annuelle.append(0)
            surplus_capital = capital * rendement_marche / 100
            capital_ajoute.append(surplus_capital)
            capital += surplus_capital
        else:
            if not ne_pas_depenser_plus_que_rendement_retraite:
                rente_annuelle.append(capital * rendement_mensuel * 12)
                capital_ajoute.append(0)
            else:
                retour_annuel_capital = capital * rendement_mensuel * 12
                rente_annuelle_depensee = min(
                    retour_annuel_capital,
                    rente_annuelle_rachat_trimestres,
                )
                surplus_capital = retour_annuel_capital - rente_annuelle_depensee
                capital += surplus_capital
                rente_annuelle.append(rente_annuelle_depensee)
                capital_ajoute.append(surplus_capital)

    return pd.DataFrame(
        index=list(range(age_investissement, age_limite_simulation + 1)),
        data={
            "Rente annuelle marché": rente_annuelle,
            "Surplus capital": capital_ajoute,
        },
    ).astype(int)


def _rente_annuelle_cumulee_marche(
    capital: int,
    rendement_marche: float,
    age_investissement: int,
    age_depart_retraite: int,
    age_limite_simulation: int,
    depenser_a_partir_de_la_retraite: bool,
    rente_mensuelle_retraite: int,
    ne_pas_depenser_plus_que_rendement_retraite: bool,
) -> pd.DataFrame:
    rente_annuelle = _rente_annuelle_marche(
        capital,
        rendement_marche,
        age_investissement,
        age_depart_retraite,
        age_limite_simulation,
        depenser_a_partir_de_la_retraite,
        rente_mensuelle_retraite,
        ne_pas_depenser_plus_que_rendement_retraite,
    )
    rente_annuelle_cum = rente_annuelle.apply(lambda col: col.cumsum(), axis=0)
    rente_annuelle_cum = rente_annuelle_cum.rename(
        columns={
            "Rente annuelle marché": "Rente annuelle cumulée marché",
            "Surplus capital": "Surplus capital cumulé",
        },
    )
    return rente_annuelle_cum
