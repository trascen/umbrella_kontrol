import mido

controls_by_name = {}

class Slider:
    def __init__(self, name, min_value=0, max_value=127):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.value = 0
        self.callback = None
        controls_by_name[name] = self

    def set_raw_value(self, value):
        self.value = (value - self.min_value) / (self.max_value - self.min_value)
        if self.callback:
            self.callback(self.value)

    def __str__(self):
        return self.name + ': ' + str(self.value)    
    
class Button:
    def __init__(self, name):
        self.name = name
        self.is_pressed = False
        self.callback = None
        controls_by_name[name] = self

    def set_raw_value(self, value):
        self.is_pressed = value == 127
        if self.callback:
            self.callback(self.is_pressed)
    
    def __str__(self):
        return self.name + ': ' + str(self.is_pressed)

korg_nano_control_map = [
 None,
 None,
 Slider('Slider 1'),
 Slider('Slider 2'),
 Slider('Slider 3'),
 Slider('Slider 4'),
 Slider('Slider 5'),
 None,
 Slider('Slider 6'),
 Slider('Slider 7'),
 None,
 None,
 Slider('Slider 8'),
 Slider('Slider 9'),
 Slider('Knob 1'),
 Slider('Knob 2'),
 Slider('Knob 3'),
 Slider('Knob 4'),
 Slider('Knob 5'),
 Slider('Knob 6'),
 Slider('Knob 7'),
 Slider('Knob 8'),
 Slider('Knob 9'),
 Button('Button 1 - Top'),
 Button('Button 2 - Top'),
 Button('Button 3 - Top'),
 Button('Button 4 - Top'),
 Button('Button 5 - Top'),
 Button('Button 6 - Top'),
 Button('Button 7 - Top'),
 Button('Button 8 - Top'),
 Button('Button 9 - Top'),
 None, #32
 Button('Button 1 - Bottom'),
 Button('Button 2 - Bottom'),
 Button('Button 3 - Bottom'),
 Button('Button 4 - Bottom'),
 Button('Button 5 - Bottom'),
 Button('Button 6 - Bottom'),
 Button('Button 7 - Bottom'),
 Button('Button 8 - Bottom'),
 Button('Button 9 - Bottom'),
]

def process_message(msg):
    if len(korg_nano_control_map) <= msg.control or korg_nano_control_map[msg.control] == None:
        print('Unknown control: ' + str(msg.control))
        return
    control = korg_nano_control_map[msg.control]
    control.set_raw_value(msg.value)

def register_control_callback(name, cb):
    if not name in controls_by_name:
        print('control ' + name + ' not found')
        return
    controls_by_name[name].callback = cb

def listen_to_kontrol():
    controls_by_name = { }

    inputs = [ n for n in mido.get_input_names() if not 'Midi Through' in n ]
    to_open = inputs[0]

    print('Opening ' + to_open)
    with mido.open_input(inputs[0]) as midi_in:
        for msg in midi_in:
            process_message(msg)