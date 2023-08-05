# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.track import Track
from warpseq.api.interfaces.base import CollectionApi

class Tracks(CollectionApi):

    object_class    = Track
    public_fields   = [ 'name', 'instrument', 'track' ]
    song_collection = 'tracks'
    add_method      = 'add_tracks'
    add_required    = [ 'muted' ]
    edit_required   = [ ]
    remove_method   = 'remove_track'
    nullable_edits  = [ ]

    def add(self, name, instrument:str=None, instruments:list=None, muted:bool=False):
        if not (instrument or instruments):
            raise InvalidUsage("either instrument or instruments is required")
        if instruments is None:
            instruments = []
        instruments = [ self.api.instruments.lookup(x, require=True) for x in instruments ]
        instrument = self.api.instruments.lookup(instrument, require=True)
        return self._generic_add(name, locals())

    def edit(self, name, new_name:str=None, instrument:str=None, instruments:list=None, muted:bool=False):
        instrument = self.api.instruments.lookup(instrument, require=False)
        if instruments is not None:
            instruments = [self.api.instruments.lookup(x, require=True) for x in instruments]
        return self._generic_edit(name, locals())