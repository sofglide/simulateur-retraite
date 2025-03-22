# -*- coding: utf-8 -*-
from src.constants import load_constants

__all__ = ["constants", "settings"]

from src.settings import load_settings

constants = load_constants()
settings = load_settings()
