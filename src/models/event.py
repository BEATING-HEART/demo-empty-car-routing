
class Event:
    def __init__(self, _from, _to, _time, _etype):
        self._from = _from
        self._to = _to
        self._time = _time
        self._etype = _etype

    def __repr__(self):
        return 'Event(from{!r}, to{!r}, etype{!r})'.format(self._from, self._to, self._etype)