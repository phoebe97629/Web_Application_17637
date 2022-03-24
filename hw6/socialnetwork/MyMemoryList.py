from threading import Lock
from copy import copy


class MyMemoryList:
    def __init__(self):
        self._list = []
        self._lock = Lock()

    def create(self, item):
        my_copy = copy(item)
        with self._lock:
            self._list.append(my_copy)
            my_copy['id'] = len(self._list)
            item['id'] = len(self._list)

    def read(self, my_id):
        if my_id is None or not isinstance(my_id, int):
            raise ValueError(f"Invalid type for id: {my_id}")

        # Since there is no deleting, id is one greater than the location of the item
        with self._lock:
            if my_id < 1 or my_id > len(self._list):
                return None

            return copy(self._list[my_id-1])

    def update(self, item):
        my_copy = copy(item)

        if 'id' not in my_copy:
            raise ValueError("Item has no 'id' attribute")

        my_id = my_copy['id']

        if my_id is None or not isinstance(my_id, int):
            raise ValueError(f"Invalid type for id: {my_id}")

        with self._lock:
            # Since there is no deleting, id is one greater than the location of the item
            if my_id < 1 or my_id > len(self._list):
                raise ValueError(f"Invalid value for id: {my_id}")

            self._list[my_id-1] = my_copy

    def match(self, last):
        if not last or not isinstance(last, str):
            raise ValueError(f"Invalid value for last: {last}")

        with self._lock:
            matches = []
            for item in self._list:
                if 'last_name' in item and item['last_name'].lower().startswith(last.lower()):
                    matches.append(copy(item))
            return matches
