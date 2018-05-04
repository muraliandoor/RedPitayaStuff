from redpitaya.overlay.mercury import mercury as overlay
import numpy as np

fpga = overlay()

#Oscilloscope code

osc0 = fpga.osc(0, 1.0)
osc0.decimation = 20
osc0.trigger_pre = 0
osc0.trigger_post = osc0.buffer_size
print ("osc0 buffer size:", osc0.buffer_size)

osc0.trig_src = 0

osc0.reset()
osc0.start()
osc0.trigger()

np.save("testoutput", osc0.data(osc0.buffer_size))
