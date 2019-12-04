try:
    import fluidsynth
except:
    print('unable to import fluidsynth module')


class midiDevice:
    def __init__(self):
        try:
            self.fs = fluidsynth.Synth()
            self.fs.start(driver="alsa")
            print("FluidSynth Started")
            self.sfid = self.fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
            self.fs.program_select(0, self.sfid, 0, 0)
        except:
            self.fs = None
    def __del__(self): # See:https://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python/
        self.fs.delete()
        print("FluidSynth Closed")
        del self.fs

    def midievent(self, buf):
        if self.fs != None:
            st = buf[0]
            ev = (buf[0] >> 4) & 0xF
            ch = buf[0] & 0xF

            if ev == 0x8: # Note Off (3 bytes : 8n note velocity)
                self.fs.noteoff(ch, buf[1])
            elif ev == 0x9: # Note On (3 bytes : 9n note velocity)
                self.fs.noteon(ch, buf[1], buf[2])
            elif ev == 0xA: # Polyphonic Pressure / Key pressure message / Aftertouch message (3 bytes : An note pressure)
                #fluid_synth_key_pressure(synth, chan, fluid_midi_event_get_key(event), fluid_midi_event_get_value(event));
                pass
            elif ev == 0xB: # Controller (3 bytes : Bn controller value)
                self.fs.cc(ch, buf[1], buf[2])
            elif ev == 0xC: # Program Change (2 bytes : Cn program)
                self.fs.program_select(ch, self.sfid, 0, buf[1])
            elif ev == 0xD: # Channel Pressure (2 bytes : Dn pressure)
                #fluid_synth_channel_pressure(synth, chan, fluid_midi_event_get_program(event));
                pass
            elif ev == 0xE: # Pitch Bend (3 bytes : En lsb msb)
                val = buf[2]*128 + buf[1] # MIDI pitch bend value (0-16383 with 8192 being center) 
                self.fs.pitch_bend(ch, val - 8192)
            elif st == 0xF0: # SysEx events (F0 length message)
                #fluid_synth_sysex(synth, event->paramptr, event->param1, NULL, NULL, NULL, FALSE);
                pass
            elif st == 0xF7: # Escape sequences (F7 length bytes)
                pass
            elif st == 0xFF: # MIDI Reset message
                self.fs.program_reset()

    def mididataset1(self, address, data):
        pass

    def close(self):
        pass
