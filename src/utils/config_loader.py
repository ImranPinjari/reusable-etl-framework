from pathlib import Path
import yaml


class ConfigLoader:

    def __init__(self, config_path="config/config.yaml"):
        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        with open(self.config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file) or {}

    def get_config(self):
        return self.config

    def get_dataset_schema(self, dataset_name):
        schema_path = (
            Path("config/schemas") / f"{dataset_name}.yaml"
        )

        if not schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {schema_path}"
            )

        with open(schema_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}
