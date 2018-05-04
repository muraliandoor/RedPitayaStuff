from redpitaya.overlay.mercury import mercury as overlay
fpga = overlay()

# First output code
gen0 = fpga.gen(0)
gen0.amplitude = 1.0
gen0.offset = 0.0
gen0.phase = 90
gen0.waveform = gen0.sin()

gen0.mode = 'PERIODIC'
gen0.frequency = 2e3

print ("Output 0 frequency:", gen0.frequency)

#First output get it running
gen0.reset()
gen0.start()
gen0.enable = True
gen0.trigger()

#Oscilloscope code

osc0 = fpga.osc(0, 1.0)
osc0.trigger_pre = 0
osc0.trigger_post = osc0.buffer_size
print ("osc0 buffer size:", osc0.buffer_size)

osc0.trig_src = 0

osc0.reset()
osc0.start()
osc0.trigger()

import matplotlib.pyplot as plt

plt.plot(osc0.data(osc0.buffer_size))
plt.show()
