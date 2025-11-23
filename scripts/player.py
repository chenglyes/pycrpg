from .role import Role
from .rolecollections import RoleCollections
from datetime import datetime
import uuid

class Player:
    def __init__(self, name: str, /, uid: str | None = None, create_time: datetime | None = None):
        self.name = name
        self.uid = uid if uid else str(uuid.uuid4())
        self.create_time = create_time if create_time else datetime.now()
        self.role_collections = RoleCollections()
        
    def add_role(self, role: Role):
        self.role_collections.add_role(role)

    def remove_role(self, role: Role):
        self.role_collections.remove_role(role)

    def get_role(self, uid: str) -> Role:
        return self.role_collections.get_role(uid)

    def to_saved(self) -> dict:
        return {
            "uid": self.uid,
            "name": self.name,
            "create_time": self.create_time.isoformat(" ", "seconds"),
            "roles": [r.to_saved() for r in self.role_collections.roles]
        }
    
    @classmethod
    def from_saved(cls, data: dict) -> "Player":
        player = Player(data["name"], uid=data["uid"], create_time=datetime.fromisoformat(data["create_time"]))
        roles = data["roles"]
        for r in roles:
            role = Role.from_saved(r)
            player.add_role(role)
        return player
    