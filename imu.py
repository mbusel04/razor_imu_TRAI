
import time
import serial


SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_BOUNDRATE = 57600

class RazorIMU():
    def __init__(self):
        self.on = False

        self.accel = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.gyro = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.mag = {'x': 0., 'y': 0., 'z': 0.}
        self.temp = None

        try:
            self.ser_ = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_BOUNDRATE, timeout=1)
            print("Connection: OK")
            self.on = True
            self.ser_.write(('#o0').encode("utf-8"))
            discard = self.ser_.readline() # Flushing output

            self.ser_.write(('#ox').encode("utf-8"))
            self.ser_.write(('#o1').encode("utf-8"))
        except:
            print("Couldn't connect to serial")
    
    def update(self):
        while(self.on):
            self.poll()
    
    def poll(self):
        try:
            line = bytearray(self.ser_.readline()).decode("utf-8")
            line = line.split('=')[1]
            values = [float(val) for val in line.split(',')]
            self.accel = { 'x' : values[3], 'y' : values[4], 'z' : values[5]}
            self.gyro = { 'x' : values[6], 'y' : values[7], 'z' : values[8]}
        except:
            print("Can't read data")
    
    def run_thread(self):
        return self.accel['x'], self.accel['y'], self.accel['z'], self.gyro['x'], self.gyro['y'], self.gyro['z'], self.temp
    
    def run(self):
        self.poll()
        return self.run_thread()
    
    def shutdown(self):
        self.on = False
    
if __name__ == "__main__":
    razor_imu = RazorIMU()
    razor_imu.update()
    razor_imu.on = False


# TODO
#   Callibration stuff
#   Checks for SERIAL_PORT
#   Arguments