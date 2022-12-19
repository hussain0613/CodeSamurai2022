import json

def get_config() -> dict:
    with open("settings.json") as f:
        settings = json.load(f)
    return settings


def get_cors_settings() -> dict:
    
    try:
        with open("cors_settings.json") as f:
            cors_settings = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        cors_settings = {
            "origins": ["*"],
            "credentials": False,
            "methods": ["*"],
            "headers": ["*"],
        }
        with open("cors_settings.json", "w") as f:
            json.dump(cors_settings, f)
    
    return cors_settings