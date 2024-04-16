from queue import Queue
from typing import Any
from app.api.helpers.threadsafe_singleton_meta import ThreadsafeSingletonMeta

class _EventData(metaclass=ThreadsafeSingletonMeta):
    """
    Event data handler that enables passing data along with tkinter virtual events.
    This functionality is missing in the Python implementation of tkinter.
    This threadsafe global singleton enables virtual event triggers to save custom event data that can be retrieved in event handlers.
    """
    context: str
    data: dict[str, dict[str, Queue]] # { context: { event_name: Queue() }}

    def __init__(self):
        self.data = {}

    def set(self, context: str, event_name: str, data: Any):
        ctx = context

        if not ctx in self.data:
            self.data[ctx] = {}

        if not event_name in self.data[ctx]:
            self.data[ctx][event_name] = Queue()

        self.data[ctx][event_name].put(data)

    def get(self, context: str, event_name: str):
        ctx = context

        if not ctx in self.data:
            return None

        if not event_name in self.data[ctx]:
            return None

        v = self.data[ctx][event_name].get()
        # logging.debug(f'EVENTDATA {context} {event_name}: {v}')
        return v


#Initialize singleton
EventData = _EventData()
