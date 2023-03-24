import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESSOURCE_DIR = BASE_DIR / "ressource"
SETTING_JSON = BASE_DIR / "settings.json"
DEFAULT_SETTING = {"unit_default": "Coups",
                   "time_default": 50,
                   "unit_list": ["Coups", "Coups/s", "Coups/min"]}


def write_json_settings(settings: dict):
    """Saves in a json file the parameters as a dictionary"""

    with open(SETTING_JSON, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)


def get_settings() -> dict:
    """Returns all settings"""

    with open(SETTING_JSON, 'r', encoding='utf-8') as f:
        content = json.load(f)

    return content


def set_default_settings(setting: str, value):
    """Replaces in the settings file, the default setting"""

    content = get_settings()
    content[setting] = value
    write_json_settings(content)


if __name__ == '__main__':
    write_json_settings(DEFAULT_SETTING)
    print(get_settings())
    set_default_settings("time_default", 400)
    print(get_settings())
