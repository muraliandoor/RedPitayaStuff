from redpitaya.overlay.mercury import mercury as overlay

# PID functions
SAMPLE_RATE = 125e6 # samples per second

SET_POINT = 0 # Volts
P_FACTOR = 4
I_FACTOR = 10 # us
D_FACTOR = 100 # us

MAX_SAMPLES = round(SAMPLE_RATE/1e6 * max(D_FACTOR, I_FACTOR))

def derivative(data):
    # Calculate number of samples in the derivative
    num_samples = round(SAMPLE_RATE/1e6 * D_FACTOR)

    return -(data[-1] - data[-num_samples]) / D_FACTOR

def integral(data):
    # Calculate number of samples in the derivative
    num_samples = round(SAMPLE_RATE/1e6 * I_FACTOR)

    dt = I_FACTOR / num_samples
    error = sum((SET_POINT - data[-i] for i in range(num_samples)))

    return error * dt

def proportional(data):
    return (SET_POINT - data[-1]) * P_FACTOR

# Set up inputs and outputs
fpga = overlay()

measurement = fpga.osc(0, 1.0)
output = fpga.gen(1)

# Set up output settings
output.mode = "BURST"
output.amplitude = 1
output.offset = 0
output.waveform = [0] # Output a constant signal
output.burst_data_repetitions = 1
output.burst_data_length = 1
output.burst_period_length = 1
output.burst_period_number = 0
output.enable = True
output.reset()
output.start()
output.trigger()

# Set up measurement
measurement.decimation = 1
measurement.trigger_pre = 0
measurement.trigger_post = MAX_SAMPLES
measurement.trig_src = 0
measurement.reset()
measurement.start()
measurement.enable = True

# Run PID loop
i=0
while True:
    i+=1
    measurement.trigger() # Start collection
    while (measurement.status_run()): pass # Wait for data
    data = measurement.data(MAX_SAMPLES) # Read data
    correction = (proportional(data) + derivative(data) + integral(data))/500
    output.offset = data[-1] + correction
    output.trigger()
    measurement.reset()
    measurement.start()
