import subprocess

pin_list_file = "pin_list.txt"

pins = []
with open(pin_list_file, 'r') as f:
	for row in f.readlines():
		pins.append(int(row))

#basic_call_string = 'cat /sys/kernel/debug/pinctrl/44e10800.pinmux/pins'
pins_status_raw = subprocess.check_output(['cat', '/sys/kernel/debug/pinctrl/44e10800.pinmux/pins'])

pins_stats_lines = pins_status_raw.split('\n')[1:-1]
labels = ['foo1', 'pin', 'memory', 'register', 'info']
pins_stats = [dict(zip(labels, line.split(' '))) for line in pins_stats_lines]

for pin in pins_stats:
	pin.pop('foo1')
	pin['pin'] = int(pin['pin'])
	pin['memory'] = int(pin['memory'][1:-1], 16)
	pin['register'] = int(pin['register'][6:], 16)

pins_stats = [pin for pin in pins_stats if pin['pin'] in pins]

slewctrl_mask  = 0b1000000
rxactive_mask  = 0b1000000
putypesel_mask = 0b0010000
puden_mask     = 0b0001000
mmode_mask     = 0b0000111

for pin in pins_stats:
	slewctrl  = (pin['register'] & slewctrl_mask) >> 6
	rxactive  = (pin['register'] & rxactive_mask) >> 5
	putypesel = (pin['register'] & putypesel_mask) >> 4
	puden     = (pin['register'] & puden_mask) >> 3
	mmode     = pin['register'] & mmode_mask

	print('Pin: {} Slew: {} ReceiverActive: {} PullUpDown: {} PUEn: {} Mux: {}'.format(pin['pin'], slewctrl, rxactive, putypesel, puden, mmode))