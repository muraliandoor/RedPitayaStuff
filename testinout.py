import numpy as np
from redpitaya.overlay.mercury import mercury as overlay

fpga = overlay()

gen0 = fpga.gen(0)

gen0.amplitude = 1.0
gen0.offset = 0.0
gen0.waveform = gen0.sin()

gen0.mode = 'PERIODIC'
gen0.frequency = 2e3

print ("Output 0 frequency:", gen0.frequency)

gen0.reset()
gen0.start()
gen0.enable = True
gen0.trigger()

#Oscilloscope Code
osc0 = fpga.osc(0, 1.0)
osc0.decimation = 20
osc0.trigger_pre = 0
osc0.trigger_post = osc0.buffer_size
print ("osc0 buffer size:", osc0.buffer_size)

osc0.trig_src = 0

osc0.reset()
osc0.start()
osc0.trigger()

data = osc0.data(osc0.buffer_size)

gen1 = fpga.gen(1)
gen1.mode = 'BURST'
gen1.ampliutde = 1.0
gen1.offset = 0
gen1.waveform = data
gen1.burst_data_repetitions = 1
gen1.burst_data_length = len(data)
gen1.burst_period_length = len(data)
gen1.burst_period_number = 0
gen1.enable = True
gen1.reset()
gen1.start()
gen1.trigger()
input()
