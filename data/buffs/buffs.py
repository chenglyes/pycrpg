from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.buff import Buff
else:
    from buff import Buff

class Burn(Buff):
    def on_apply(self, actor, context):
        pass
