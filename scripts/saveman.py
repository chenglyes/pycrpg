from .player import Player
from dataclasses import dataclass
import os
import json

@dataclass
class PlayerView:
    uid: str
    name: str
    create_time: str

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "create_time": self.create_time
        }

class SaveMan:
    def __init__(self):
        self.player_views: list[PlayerView] = []
        self.load()

    def save(self):
        os.makedirs("user", exist_ok=True)
        with open("user/player.json", "w", encoding="utf-8") as f:
            views = [v.to_dict() for v in self.player_views]
            json.dump(views, f, indent=4)

    def load(self):
        self.player_views = []
        try:
            with open("user/player.json", "r", encoding="utf-8") as f:
                root = json.load(f)
                for data in root:
                    self.player_views.append(PlayerView(**data))
        except FileNotFoundError:
            pass

    def update_view(self, player: Player):
        view = PlayerView(player.uid, player.name, player.create_time.isoformat())
        has = False
        for v in self.player_views:
            if v.uid == player.uid:
                v = view
                has = True
                break
        if not has:
            self.player_views.append(view)

    def save_player(self, player: Player):
        os.makedirs(f"user/players", exist_ok=True)
        with open(f"user/players/{player.uid}.json", "w", encoding="utf-8") as f:
            json.dump(player.to_saved(), f, indent=4)
            self.update_view(player)
            self.save()

    def load_player(self, uid: str)  -> Player:
        with open(f"user/players/{uid}.json", "r", encoding="utf-8") as f:
            return Player.from_saved(json.load(f))
