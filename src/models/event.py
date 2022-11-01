
class Event:
    def __init__(self, from_, to_, etype_):
        self.from_ = from_
        self.to_ = to_
        self.etype_ = etype_

    def __repr__(self):
        return 'Event({!r})'.format(self.etype_)