# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class is used by the player code to send MIDI events to hardware
# it contains some logic to convert chords to note events and must also
# process deferred mod-expressions caused by late-binding intra-track
# events.

from warpseq.api.callbacks import Callbacks
from warpseq.api.exceptions import *
from warpseq.model.registers import register_playing_note, unregister_playing_note
from warpseq.playback.midi import midi_note_on, midi_note_off, midi_cc
from warpseq.model.chord import Chord
from warpseq.model.event import Event, NOTE_OFF, NOTE_ON

def _get_note_number(note, instrument):

    max_o = instrument.max_octave
    min_o = instrument.min_octave

    note2 = note.transpose(octaves=instrument.base_octave)

    if note2.octave > max_o:
        note2.octave = max_o
    if note2.octave < min_o:
        note2.octave = min_o

    nn = note2.note_number()

    if nn < 0 or nn > 127:
        print("warning: note outside of playable range: %s" % note)
        return None

    return nn


class RealtimeEngine(object):

    __slots__ = ['song','track','clip','midi_out','midi_port','mod_expressions','callbacks','on_count','player']

    def __init__(self, song=None, track=None, clip=None, player=None):
        self.song = song
        self.track = track
        self.clip = clip
        self.player = player
        self.callbacks = Callbacks()

    def play(self, event):

        # deferred events happen when there are intra-track events such as replacing the note
        # with the currently playing note from a guide track (see docs). In this case we must
        # re-evaluate all mod expressions... we do not need to re-evaluate the track expressions
        # because the mod expression does throw away the note value and capture the value from
        # the guide track...

        pattern = event.note.from_context.pattern

        cb = pattern.mod_expressions_callback # this must be a generator

        if event.type == NOTE_ON:

            # we have to process deferred expressions twice because of the mod events
            # UNLESS we pair the off event.

            #self.context.scale = event.scale
            #self.context.pattern = event.from_context.pattern

            exprs = event.note.deferred_expressions
            for expr in exprs:
                value = expr.evaluate(self.track, event.note)
                if value is None:
                    return
                event.note = value

            # run mod expressions callback if attached
            if cb is not None:
                new_mod_expressions = next(cb)
                for expr in new_mod_expressions:
                    event.note = expr.evaluate(self.track, event.note)
                    if event.note is None:
                        return
                    event.note = value

                    # not entirely sure how this happens but we need to guard against it for now
                    # this really should be part of "mod_expressions.do"
                    if type(value) == Chord and len(value.notes) == 1:
                        event.note = value.notes[0]

        # it is possible for mod expressions to take notes and return Chords. We have to do
        # cleanup here to turn this back into a list of notes.

        if type(event.note) == Chord:
            for x in event.note.notes:
                evt = event.copy()
                evt.note = x
                evt.note.deferred = False
                self.play(evt)
            return

        if not event.note:
            return

        if event.type == NOTE_ON:

            # FIXME: assign note vs always redeferencing event.note

            velocity = event.note.velocity
            if velocity is None:
                velocity = self.instrument.default_velocity

            register_playing_note(self.track, event.note)

            for (control, value) in event.note.ccs.items():
                control = int(control)
                for instrument in self.track.get_instruments_to_play():
                    midi_cc(instrument.get_midi_out(), instrument.channel, control, int(value))


            if not (self.track.muted or event.note.muted):
                self.player.inject_off_event(event)
                for instrument in self.track.get_instruments_to_play():
                    if not instrument.muted:
                        #print("PLAY: %s / %s" % (instrument.name, event.note))
                        midi_note_on(instrument.get_midi_out(), instrument.channel, _get_note_number(event.note, instrument), velocity)


        elif event.type == NOTE_OFF:

            # similar logic to the above: there is a chance we have an event tied to a chord, and we then need to silence
            # all notes in that chord separately.

            if type(event.on_event.note) == Chord:
                for x in event.on_event.note.notes:
                    evt = event.copy()
                    evt.on_event = Event(time = event.on_event.time, scale=event.scale, note = x, type=event.on_event.type, on_event=None)
                    self.play(evt)
                return

            velocity = event.note.velocity
            if velocity is None:
                velocity = self.instrument.default_velocity

            unregister_playing_note(self.track, event.on_event.note)

            if self.track.muted:
                return
            for instrument in self.track.get_instruments_to_play():
                if not instrument.muted:
                    midi_note_off(instrument.get_midi_out(), instrument.channel,  _get_note_number(event.note, instrument), velocity)

