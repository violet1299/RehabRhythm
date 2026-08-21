import json
import os

from config import *


class SettingsManager:
    def __init__(self, path="data/settings.json"):
        self.path = path

    def load(self):
        default_settings = {
            "music_volume": DEFAULT_MUSIC_VOLUME,
            "sound_volume": DEFAULT_SOUND_VOLUME,
            "show_fps": DEFAULT_SHOW_FPS
        }

        if not os.path.exists(self.path):
            return default_settings

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)

            default_settings["music_volume"] = float(
                data.get("music_volume", DEFAULT_MUSIC_VOLUME)
            )
            default_settings["sound_volume"] = float(
                data.get("sound_volume", DEFAULT_SOUND_VOLUME)
            )
            default_settings["show_fps"] = bool(
                data.get("show_fps", DEFAULT_SHOW_FPS)
            )

            return default_settings

        except Exception:
            return default_settings

    def save(self, music_volume, sound_volume, show_fps):
        os.makedirs("data", exist_ok=True)

        data = {
            "music_volume": round(music_volume, 2),
            "sound_volume": round(sound_volume, 2),
            "show_fps": show_fps
        }

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def reset(self):
        self.save(
            DEFAULT_MUSIC_VOLUME,
            DEFAULT_SOUND_VOLUME,
            DEFAULT_SHOW_FPS
        )