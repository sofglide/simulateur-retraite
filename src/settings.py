# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


class GlobalSettingsConfig(BaseModel):
    salaire_base: int = Field(default=3000)
    cout_trimestre: int = Field(default=2500)


class CalculMontantRetraiteSettingsConfig(BaseModel):
    nombre_annees_simulation: tuple[int, int] = Field(default=(25, 35))
    affichage_calcul_retraite: int = Field(default=2)


class ComparaisonRachatVsInvestissementSettingsConfig(BaseModel):
    age_rachat_trimestres: int = Field(default=55)
    age_depart_retraite: int = Field(default=65)
    nombre_trimestres_rachetes: int = Field(default=12)
    nombre_annees_travaillees: int = Field(default=35)
    rendement_attendu_du_marche: float = Field(default=5.0)
    age_limite_simulation: int = Field(default=80)
    depenser_a_partir_de_la_retraite: bool = Field(default=True)
    depenser_equiv_rachat_trimestre: bool = Field(default=False)
    afficher_valeurs_cumulees: bool = Field(default=True)


class SettingsConfig(BaseModel):
    """Constants object."""

    global_params: GlobalSettingsConfig = Field(default_factory=GlobalSettingsConfig)
    calcul_montant_retraite: CalculMontantRetraiteSettingsConfig = Field(
        default_factory=CalculMontantRetraiteSettingsConfig,
    )
    comparaison_rachat_vs_investissement: ComparaisonRachatVsInvestissementSettingsConfig = Field(
        default_factory=ComparaisonRachatVsInvestissementSettingsConfig,
    )


def load_settings() -> SettingsConfig:
    """Load user settings."""
    return SettingsConfig()
