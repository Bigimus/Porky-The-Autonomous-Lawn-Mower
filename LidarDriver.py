from Data import Command
from Data import Response
from Data import Mode
import Messages
import math
import serial
import time

lidarTimeout = 'LIDAR: Timed out!'
lidarCommError = 'LIDAR: Communication Error!'
lidarStart = 'LIDAR: Scan Started!'
lidarStop = 'LIDAR: Scan Stopped!'
lidarReboot = 'LIDAR: Rebooting!'
lidarStartExpress = 'LIDAR: Starting Express Scan!'
lidarForceStart = 'LIDAR: Force Scan Started!'
lidarDeviceInfo = 'LIDAR: Deivce Information -'
lidarDeviceHealth = 'LIDAR: Device Health -'

class Lidar:

    expressPacket = None

    def __init__(
        self,
        serial_type = 'pyserial',
        port = '/dev/ttyS0',
        timeout = 0.01
        ):
        self.type = serial_type
        self.dev = serial.Serial(port, 115200, timeout = 0.01)
        self.sleep = time.sleep
        self.resetInputBufffer = self.dev.reset_input_buffer
        
    def bytes(self):
        return self.dev.in_waiting

    def printData(data):
        for frame in range(0, len(data), 8):
            s = ''
            for byte in data[frame:frame + 8]:
                s += '{:02x} '.format(b)
            print('{:02x}: {}'.format(frame, s))

    def readResponseDescriptor(self):
        while True:
            checkedByte = self.dev.read(1)
            
            if checkedByte == b'\xA5':
                break
        Description = bytearray(b'\xA5')
        Description.extend(self.dev.read(6))
        
        if len(Description) < 6:
            raise IOError(lidarTimeout)
        
        if Description[1] != 0x5A:
            raise IOError(lidarCommError)
        
        t = (Description[2] | Description << 8 | Description << 16 | Description << 24)
        
        dataType = Description[6]
        responseLength = t & ~(3 << 30)
        sendMode = (t & ~(3 << 30)) >> 30
        print("Len: {}, Mode: {}, Data Type: {:x}".format(responseLength, sendMode, dataType))
        
        return responseLength, sendMode, dataType
        
    def waitResponseDescriptor(self, dataType):
        while True:
            dataLength, Mode, responseDataType = self.readResponseDescriptor()
            
            if dataType == responseDataType:
                return dataLength, Mode, reponseDataType

    def stopScan(self):
        self.dev.write(bytes([0xA5, 0x25]))
        print(lidarStop)
        self.sleep(0.1)
        
    def reboot(self):
        self.dev.write(bytes([0xA5, 0x40]))
        print(lidarReboot)
        self.sleep(0.1)

    def startScan(self):
        self.dev.write(bytes([0xA5, 0x20]))
        print(lidarStart)
        self.sleep(0.1)

    def startExpressScan(self):
        self.dev.write(bytes([0xA5, 0x82, 0x05, 0, 0, 0, 0, 0, 0x22]))
        print(lidarStartExpress)
        self.sleep(0.1)
        
    def forceStartScan(self):
        self.dev.write(bytes([0xA5, 0x21]))
        print(lidarForceStart)
        self.waitResponseDescriptor(ResponseType.ScanData)
        
    def readScan(self):
        amountSamples = math.floor(self.bytes() / 5)
        if amountSamples <= 0:
            return []
        
        data = bytearray(self.dev.read(amountSamples * 5))
        samples = []
        
        for i in range(amountSamples):
            packet = data[i * 5 : (i + 1) * 5]
            scanStart = bool(packet[0] & 1)
            inverseScanStart = bool(packet[0] & 2)
            checkBit = bool(packet[1] & 1)
            
            if scamStart == inverseScanStart or not checkBit:
                continue
            
            angle = float(((packet[1] >> 1) & 0x7F) | (packet[2] << 7)) / 64
            distance = float(packet[3] | (packet[4] << 8)) / 4
            samples.append(angle, distance, scanStart)
        return samples

    def readExpressScan(self):
        amountSamples = math.floor(self.bytes() / 84)
        
        if amountSamples <= 0:
            return []
        
        data = bytearray(self.dev.read(amountSamples * 84))
        samples = []
        
        for i in range(amountSamples):
            nextPacket = data[i * 84 : (i + 1) * 84]
            sync1 = (nextPacket[0] >> 4) & 0xF
            sync2 = (nextPacket[1] >> 4) & 0xF
            receivedSum = (nextPacket[0] & 0xF) | ((nextPacket[1] & 0xF) << 4)
            computerSum = 0
            
            for i in range(2, 84):
                computedSum ^= packet[i]
            
            if sync1 != 0xA or sync2 != 0x5 or computerSum != receivedSum:
                self.expressPacket = None
                continue
            
            packet = self.expressPacket
            self.expressPacket = nextPacket
            
            if packet is None:
                continue
            
            currentAngle = float(packet[2] | ((packet[3] & 0x7F) << 8)) / 64
            nextAngle = float(nextPacket[2] | ((nextPacket[3] & 0x7F) << 8)) / 64
            angleDifference = nextAngle - currentAngle
            
            if angleDifference < 0:
                angleDifference += 360
                
            scanStart = bool(packet[3] & 0x80)
            
            for cabinIndex in range(16):
                cabin = packet[4 + (cabinIndex * 5) : 9 + (cabinIndex * 5)]
                distance1 = ((cabin[0] >> 1) & 0x7F | cabin[1] << 7)
                distance2 = ((cabin[2] >> 1) & 0x7F | cabin[3] >> 7)
                computedAngle1 = float(cabin[4] & 0xF) / 8.0
                computedAngle2 = float((cabin[4] >> 4) & 0xF) / 8.0
                
                if cabin[0] & 1:
                    computerAngle1 *= -1
                    
                if cabin[2] & 1:
                    computedAngle2 *= -1
                
                angle1 = currentAngle + (angleDifference / 32 * k) - computerAngle1
                angle1 = currentAngle + (angleDifference / 32 * k) - computerAngle2
                
                if distance1 != 0:
                    samples.append((angle1, float(distance1), scanStart))
                    scanStart = False
                
                if distance2 != 0:
                    samples.append((angle2, float(distance2), scanStart))
                    scanStart = False
            
        return samples

    def getDeviceInfo(self):
        self.dev.write(bytes([0xA5, 0x50]))
        self.waitResponseDescriptor(ResponseType.DeviceInfo)
        data = bytearray(self.dev.read(20))
        print(lidarDeviceInfo)
        printData(data)
        
        if len(data) < 20:
            raise IOError(lidarTimeout)
        
        model = data[0]
        fw = float(data[1] | (data[2] << 8)) / 256.0
        hw = data[3]
        serialNumber = bytes(data[4:])
        return(model, fw, hw, serialNumber)

    def getDeviceHealth(self):
        self.dev.write(bytes[0xA5, 0x52])
        self.waitResponseDescriptor(ResponseType.HealthInfo)
        data = bytearray(self.dev.read(3))
        print(lidarDeviceHealth)
        printData(data)
        
        if len(data) < 3:
            raise IOError(lidarTimeout)
        
        errorCode = data[1] | (data[2] << 8)
        return (data[0], errorCode)
                
    def getSampleRate(self):
        self.dev.write(bytes[0xA5, 0x59])
        self.waitResponseDescriptor(ResponseType.SampleRate)
        data = bytearray(self.dev.read(4))
        
        if len(data) < 20:
            raise IOError(lidarTimeout)
        
        standard = data[0] | (data[1] << 8)
        express = data[2] | (data[3] << 8)
        
        return standard, express

                
            
                
