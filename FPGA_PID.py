import subprocess

SP_BUFFER = {(1, 1): "0x40300010", (1, 2): "0x40300020", (2, 1): "0x40300030", (2, 2): "0x40300040"}
KP_BUFFER = {(1, 1): "0x40300014", (1, 2): "0x40300024", (2, 1): "0x40300034", (2, 2): "0x40300044"}
KI_BUFFER = {(1, 1): "0x40300018", (1, 2): "0x40300028", (2, 1): "0x40300038", (2, 2): "0x40300048"}
KD_BUFFER = {(1, 1): "0x4030001c", (1, 2): "0x4030002c", (2, 1): "0x4030003c", (2, 2): "0x4030004c"}

class FPGA_PID:
    """
    Interface with the buffers that control the Red Pitaya's FPGA PID
    implementation.
    """

    def __init__(self, in_channel, out_channel, set_point, k_proportional, k_integral, k_derivative):
        self.channels = (in_channel, out_channel)

        self.set_point(set_point)
        self.proportional(k_proportional)
        self.integral(k_integral)
        self.derivative(k_derivative)

    def set_point(self, val):
        if val < -2**13 or val > 2**13 - 1:
            raise ValueError("Set point out of range.")

        self.sp = val
        subprocess.run(["monitor", SP_BUFFER[self.channels], str(val)])

    def proportional(self, val):
        if val < -2**13 or val > 2**13 - 1:
            raise ValueError("Proportional constant out of range.")

        self.kp = val
        subprocess.run(["monitor", KP_BUFFER[self.channels], str(val)])

    def integral(self, val):
        if val < -2**13 or val > 2**13 - 1:
            raise ValueError("Integral constant out of range.")

        self.ki = val
        subprocess.run(["monitor", KI_BUFFER[self.channels], str(val)])

    def derivative(self, val):
        if val < -2**13 or val > 2**13 - 1:
            raise ValueError("Derivative constant out of range.")

        self.kd = val
        subprocess.run(["monitor", KD_BUFFER[self.channels], str(val)])
