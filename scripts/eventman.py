
class EventMan:
    def __init__(self):
        self._listeners: dict[type, list] = {}

    def register(self, event_type: type, callback):
        self._listeners[event_type].append(callback)

    def dispatch(self, event):
        event_type = type(event)
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(event)
