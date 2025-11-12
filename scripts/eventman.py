class EventMan:
    def __init__(self):
        self._listeners: dict[type, list] = {}
        self._id = 0

    def register(self, event_type: type, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def dispatch(self, event):
        event_type = type(event)
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(event)
