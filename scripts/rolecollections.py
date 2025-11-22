from .role import Role

class RoleCollections:
    def __init__(self):
        self._roles: dict[str, Role] = {}

    @property
    def roles(self) -> list[Role]:
        return list(self._roles.values())
    
    def add_role(self, role: Role):
        if role.uid in self._roles:
            raise IndexError(f"Role with UID '{role.uid}' already exists.")
        self._roles[role.uid] = role
        
    def remove_role(self, role: Role):
        self._roles.pop(role.uid)

    def get_role(self, uid: str) -> Role:
        role = self._roles.get(uid)
        if role is None:
            raise IndexError(f"Role with UID '{uid}' not exists.")
        return role
    