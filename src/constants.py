# -*- coding: utf-8 -*-
import yaml
from pydantic import BaseModel, Field
from pathlib import Path


class SliderConfig(BaseModel):
    """Slider config object."""

    min_: int = Field(alias="min")
    max_: int = Field(alias="max")
    step: int


class SliderFloatConfig(BaseModel):
    """Slider config object."""

    min_: float = Field(alias="min")
    max_: float = Field(alias="max")
    step: float


class GlobalParamsConfig(BaseModel):
    salaire_base: SliderConfig
    cout_rachat_trimestre: SliderConfig


class SelectBoxConfig(BaseModel):
    options: list[str]


class CalculMontantRetraiteConfig(BaseModel):
    nombre_annees_simulation: SliderConfig
    affichage_calcul_retraite: SelectBoxConfig


class ComparaisonRachatVsInvestissementConfig(BaseModel):
    age_rachat_trimestres: SliderConfig
    age_depart_retraite: SliderConfig
    nombre_trimestres_rachetes: SliderConfig
    nombre_annees_travaillees: SliderConfig
    rendement_attendu_du_marche: SliderFloatConfig
    age_limite_simulation: SliderConfig


class Constants(BaseModel):
    """Constants object."""

    global_params: GlobalParamsConfig
    calcul_montant_retraite: CalculMontantRetraiteConfig
    comparaison_rachat_vs_investissement: ComparaisonRachatVsInvestissementConfig


def load_constants() -> Constants:
    """Load constants."""
    constants_file = Path("./config/constants.yaml")
    if not constants_file.exists():
        raise FileNotFoundError("Constants file not found.")

    return Constants(**yaml.safe_load(constants_file.read_text()))
