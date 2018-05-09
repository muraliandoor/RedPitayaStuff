import subprocess

class FPGA_PID:
    """
    Interface with the buffers that control the Red Pitaya's FPGA PID
    implementation.
    """

    SP_BUFFER = 0x40300010
    KP_BUFFER = 0x40300014
    KD_BUFFER = 0x4030001c
    KI_BUFFER = 0x40300018

    def __init__(self, set_point, k_proportional, k_derivative, k_integral):
        self.set_point(set_point)
        self.proportional(k_proportional)
        self.derivative(k_derivative)
        self.integral(k_integral)

    def set_point(self, val):
        if val < -2**13 or val > 2**13 - 1:
            raise ValueError("Set point out of range.")

        self.sp = val
        subprocess.run(["monitor", FPGA_PID.SP_BUFFER, val])

    def proportional(self, val):
        if val < -2**13 or val > 2**13 - 1:
            raise ValueError("Proportional constant out of range.")

        self.kp = val
        subprocess.run(["monitor", FPGA_PID.KP_BUFFER, val])

    def derivative(self, val):
        if val < -2**13 or val > 2**13 - 1:
            raise ValueError("Derivative constant out of range.")

        self.kd = val
        subprocess.run(["monitor", FPGA_PID.KD_BUFFER, val])

    def integral(self, val):
        if val < -2**13 or val > 2**13 - 1:
            raise ValueError("Integral constant out of range.")

        self.ki = val
        subprocess.run(["monitor", FPGA_PID.KI_BUFFER, val])
