import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESSOURCE_DIR = BASE_DIR / "ressource"
SETTING_JSON = BASE_DIR / "settings.json"
DEFAULT_SETTING = {"default": "0",
                   "0": {"analysis": "Alpha-Bêta",
                         "label1": "Coups 1 :",
                         "label2": "Coups 2 :",
                         "regex": r"[1-9]\d*"},
                   "1": {"analysis": "Tritium",
                         "label1": "CPMA 1 :",
                         "label2": "CPMA 2 :",
                         "regex": r"[1-9]?\d*((\.|,){1}\d{0,2})"}}


def write_json_settings(settings: dict):
    """Saves in a json file the parameters as a dictionary"""

    with open(SETTING_JSON, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)


def get_default_analysis_settings() -> dict:
    """Returns the default analysis settings"""

    content = get_settings()
    return content[content["default"]]


def get_settings() -> dict:
    """Returns all settings"""

    with open(SETTING_JSON, 'r', encoding='utf-8') as f:
        content = json.load(f)

    return content


def set_default_analysis_settings(default: str):
    """Replaces in the settings file, the default analysis"""

    content = get_settings()
    content["default"] = default
    write_json_settings(content)


if __name__ == '__main__':
    write_json_settings(DEFAULT_SETTING)
    set_default_analysis_settings("1")
