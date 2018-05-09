import subprocess

class FPGA_PID:
    """
    Interface with the buffers that control the Red Pitaya's FPGA PID
    implementation.
    """

    def __init__(self, set_point, k_proportional, k_derivative, k_integral):
        self.set_point(set_point)
        self.proportional(k_proportional)
        self.derivative(k_derivative)
        self.integral(k_integral)

    def set_point(self, val):
        self.sp = val
        subprocess.run(["monitor", 0x40300010, val])

    def proportional(self, val):
        self.kp = val
        subprocess.run(["monitor", 0x40300014, val])

    def derivative(self, val):
        self.kd = val
        subprocess.run(["monitor", 0x4030001c, val])

    def integral(self, val):
        self.ki = val
        subprocess.run(["monitor", 0x40300018, val])
