import time

from redpitaya.overlay.mercury import mercury as overlay
fpga = overlay()

time.sleep(1)

gen0 = fpga.gen(0)

time.sleep(1)
gen0.amplitude = 1.0
gen0.offset = 0.0
gen0.waveform = gen0.sin()

time.sleep(1)

gen0.mode = 'PERIODIC'
gen0.frequency = 2e3

print ("Output 0 frequency:", gen0.frequency)

time.sleep(1)
gen0.reset()
gen0.start()
gen0.enable = True
gen0.trigger()

x = input("")
