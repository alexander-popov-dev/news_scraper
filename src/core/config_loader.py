import importlib
import inspect
from typing import get_type_hints

from src.core.factories.dto import ScrapingConfigsDTO


class ConfigLoader:
    @staticmethod
    def load_configs(package: str) -> ScrapingConfigsDTO:
        module_path = f"src.sites.{package}.config"

        try:
            module = importlib.import_module(module_path)

            for name, obj in inspect.getmembers(module):
                if callable(obj) and not name.startswith("_"):
                    hints = get_type_hints(obj)
                    if hints.get("return") == ScrapingConfigsDTO:
                        configs = obj()
                        if isinstance(configs, ScrapingConfigsDTO):
                            return configs

            for name, obj in inspect.getmembers(module):
                if isinstance(obj, ScrapingConfigsDTO):
                    return obj

            raise ValueError(
                f"No ScrapingConfigsDTO found in {module_path}. "
                f"Expected: function returning ScrapingConfigsDTO or variable of type ScrapingConfigsDTO"
            )

        except ModuleNotFoundError as e:
            raise ValueError(f"Cannot load config from {module_path}: {e}")
