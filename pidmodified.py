from redpitaya.overlay.mercury import mercury as overlay
import numpy as np
import cProfile
import pstats

# PID functions
SAMPLE_RATE = 125e6 # samples per second

SET_POINT = 0.5 # Volts
KP = 2
KI = 2 
KD = 2 
Ti = 100 #us
Td = 10 #us

MAX_SAMPLES = round(SAMPLE_RATE/1e6 * Ti)

def derivative(data):
    # Calculate number of samples in the derivative
    num_samples = round(SAMPLE_RATE/1e6 * Td)

    return -KD * (data[-1] - data[-num_samples]) / Td 

def integral(data):
    # Calculate number of samples in the derivative
    num_samples = round(SAMPLE_RATE/1e6 * Ti)

    dt = Ti / num_samples
    error = dt * np.sum(np.array([SET_POINT]*num_samples) - (data[-num_samples:]))

    return KI * error

def proportional(data):
    return KP * (SET_POINT - data[-1])

# Set up inputs and outputs
fpga = overlay()

measurement = fpga.osc(0, 1.0)
output = fpga.gen(1)

# Set up output settings
output.mode = "BURST"
output.amplitude = 1.0
output.offset = 0
output.waveform = [0] # Output a constant signal
output.burst_data_repetitions = 1
output.burst_data_length = 1
output.burst_period_length = 1
output.burst_period_number = 0 
output.enable = True
output.reset()
output.start()

# Set up measurement
measurement.decimation = 1
measurement.trigger_pre = 0
measurement.trigger_post = MAX_SAMPLES
measurement.trig_src = 0
measurement.reset()
measurement.start()

# Run PID loop
def runff():
	for i in range(10000):
		# Collect data
		measurement.trigger() # Start collection
#		while (measurement.status_run()): pass # Wait for data
		data = measurement.data(MAX_SAMPLES) # Read data
		# Calculate correction
		correction = proportional(data)/4 #+ derivative(data) + integral(data))/500
		#print(correction)
		# Output correction
		#print("EPOCH:", i)
		output.offset = correction
		measurement.reset()
		measurement.start()
		output.trigger()

cProfile.run('runff()', 'stats')
p = pstats.Stats('stats')
p.sort_stats('cumulative')
p.print_stats()
