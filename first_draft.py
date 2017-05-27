from streamer import Streamer
from effects import *
from midi import Slider, Button, listen_to_kontrol, register_control_callback


    
streamer = Streamer()
hsvfill = HsvFillEffect()
linefx = LineScrollEffect()

streamer.effects.append(linefx)
streamer.effects.append(hsvfill)
streamer.start()

register_control_callback('Knob 1', lambda v: hsvfill.set_h(v))
register_control_callback('Knob 2', lambda v: hsvfill.set_s(v))
register_control_callback('Knob 3', lambda v: hsvfill.set_v(v))
register_control_callback('Knob 5', lambda v: linefx.set_speed(v))





listen_to_kontrol()