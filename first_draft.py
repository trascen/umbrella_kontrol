from streamer import Streamer
from effects import *
from midi import Slider, Button, listen_to_kontrol, register_control_callback
from blinkenwallctl import BlinkenwallCtl

bw = BlinkenwallCtl()
    
streamer = Streamer()
hsvfill = HsvFillEffect()
#linefx = LineScrollEffect()
rainbow = RainbowEffect()
fire = FireEffect()

#streamer.effects.append(linefx)
#streamer.effects.append(hsvfill)
streamer.effects.append(fire)


register_control_callback('Knob 1', lambda v: hsvfill.set_h(v))
register_control_callback('Knob 2', lambda v: hsvfill.set_s(v))
register_control_callback('Knob 3', lambda v: hsvfill.set_v(v))
#register_control_callback('Knob 5', lambda v: linefx.set_speed(v))
register_control_callback('Knob 5', lambda v: rainbow.set_speed(v))
register_control_callback('Knob 6', lambda v: rainbow.set_offset(v))

register_control_callback('Button Prev', lambda v: bw.send_prev(v))
register_control_callback('Button Next', lambda v: bw.send_next(v))
register_control_callback('Button Stop', lambda v: bw.send_blank(v))
register_control_callback('Button 1 - Top', lambda v: fire.shuffle(v))

streamer.start()
listen_to_kontrol()