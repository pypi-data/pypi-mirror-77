# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# various low level functions broken out of clip.py for clip evaluation
# (these could use some cleanup)

# a small gap between notes that ensures the off notes fire before the on notes
NOTE_GAP = 0.0001

from warpseq.api.exceptions import *
from warpseq.model.chord import Chord
from warpseq.model.event import NOTE_OFF, NOTE_ON, Event
from warpseq.model.note import Note

def _add_note_to_bucket(this_bucket, note, scale, t_start):

    if type(note) != Chord:
        note.from_scale = scale
        note.start_time = t_start
        note.end_time = round(t_start + note.length)
        note.from_scale = scale
        this_bucket.append(note)
    else:
        for n in note.notes:
            n.from_scale = scale
            n.start_time = t_start
            n.end_time = round(t_start + n.length)
            n.from_scale = scale
        this_bucket.append(note)

def standardize_notes(old_list, scale, slot_duration, t_start):

    results = []
    previous_notes = []

    # incoming is a list of things that happen in each slots (each is a list)
    # each item may be a list of notes
    # or a chord
    # or a list containing ONE chord - which must be broken into notes

    ts = t_start

    for obj in old_list:

        this_bucket = []
        is_tie = False

        if type(obj) == Chord:
            for note in obj.notes:
                _add_note_to_bucket(this_bucket, note, scale, ts)

        elif type(obj) == Note:
            if not obj.tie:
                _add_note_to_bucket(this_bucket, obj, scale, ts)
            else:
                is_tie = True

        elif obj is not None:
            raise Exception("unexpected: %s" % obj)

        if is_tie:
            for p in previous_notes:
                p.length = p.length + slot_duration
                p.end_time = p.end_time + slot_duration
                p.tied = p.tied + 1
        else:
            previous_notes = this_bucket

        results.append(this_bucket)

        ts = ts + slot_duration

    return results



def notes_to_events(clip, note_list): #, resolution=NOTE_RESOLUTION):

    # takes a note list like
    # [[n1, n2, n3], [n4, n5]]
    #
    # and returns a event list like:
    #
    # [e1_on, e2_on, e3_on], [], [], [e1_off, e2_off, e3_off], [], ...

    from ..model.chord import Chord
    from ..model.note import Note

    events = []


    for slot in note_list:

        for in_note in slot:

            if not in_note:
                my_notes = []
            elif type(in_note) == Note:
                my_notes = [ in_note ]
            else: # assume Chord
                my_notes = in_note.notes

            for note in my_notes:


                if note is not None and not note.tie:


                    if note.delay:
                        bump = (note.delay * note.from_parser._slot_duration)
                        note.start_time = note.start_time + bump
                        note.end_time = note.end_time + bump

                    assert note.from_context is not None
                    event1 = Event(type=NOTE_ON, note=note, time=int(note.start_time), scale=note.from_scale, from_context=note.from_context)

                    events.append(event1)



    return events
