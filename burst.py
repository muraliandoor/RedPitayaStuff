import numpy as np
from redpitaya.overlay.mercury import mercury as overlay

fpga = overlay()

SAMPLE_RATE = 125e6

def waveform(generator, wave_function, frequency, phase=0):
    """
    Calculate one period of an arbitrary wave in as high resolution as
    possible, with a variable frequency and phase shift.

    @param generator: the Red Pitaya function generator object

    @param wave_function: an arbitrary function with a period of 2pi
        and a range of [-1, 1].

    @param frequency: the target frequency, in hertz

    @param phase: phase shift in radians (default 0)
    """

    samples = round(SAMPLE_RATE / frequency) # Number of samples to make one period of the curve at 125 MSps

    compression = int(np.ceil(samples / generator.buffer_size)) # Compression factor to fit inside the buffer
    signal = list(map(wave_function, np.linspace(0-phase, 2*np.pi-phase, int(samples/compression)))) # Generate the signal

    generator.waveform = signal
    generator.burst_data_repetitions = compression # Repeat each data point to stretch the signal back out to full size
    generator.burst_data_length = len(signal)
    generator.burst_period_length = len(signal)*compression

# Set up function generators
gen0 = fpga.gen(0)
gen1 = fpga.gen(1)

# Set up burst mode
gen0.mode = "BURST"
gen1.mode = "BURST"

# Set output waveform characteristics
waveform(gen0, np.sin, 5000)
gen0.amplitude = 1.0
gen0.offset = 0
gen0.burst_period_number = 4

waveform(gen1, np.tan, 5000, np.pi)
gen1.ampliutde = 1.0
gen1.offset = 0
gen1.burst_period_number = 4

# Sync gen1 to gen0
gen1.sync_src = fpga.sync_src["gen0"]

# Start generators
gen0.enable = True
gen1.enable = True
gen0.reset()
gen0.start()

gen0.trigger()
