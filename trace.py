import rp_scpi
import math
import matplotlib.pyplot as plt

MAX_RATE = 125e6 # Full sample rate in samples per second
TRACE_TIME = 1 # Duration of the trace in seconds

# Connect to the Red Pitaya
rp = rp_scpi.scpi("rp-f05f10.local", 5000)

# Set up for data acquisition
rp.tx_txt("acq:data:units volts")
rp.tx_txt("acq:data:format ascii")

# Calculate decimation (only capture every n samples)
buffer_size = int(rp.txrx_txt("acq:buf:size?"))
sample_rate = TRACE_TIME / buffer_size # Sample rate to exactly fill the buffer for this trace time
ratio = MAX_RATE / sample_rate
decimation = round(math.log(ratio, 2))

rp.tx_txt("acq:dec {}".format(decimation)) # Set decimation

# Start acquiring data
rp.tx_txt("acq:start")
rp.tx_txt("trig now")

# Wait for acquisition to finish
while True:
    rp.tx_txt("acq:trig:stat?")
    if rp.rx_txt() == "TD":
        break

# Read the data
for channel in (1,2):
    response = rp.txrx_txt("acq:sour{}:data?".format(channel))
    response = response.strip("{}\n\r").replace("  ", "").split(",")

    data = list(map(float, response))
    plt.plot(data)

plt.ylabel("Voltage")
plt.show()
