class Command:
    Scan = 0x20
    forceScan = 0x21
    Stop = 0x25
    Reset = 0x40
    getInfo = 0x50
    getHealth = 0x52
    getSampleRate = 0x59
    expressScan = 0x82

class Response:
    deviceInfo = 0x04
    healthInfo = 0x06
    samplingRate = 0x15
    scanData = 0x81
    expressScanData = 0x82
    
class Mode:
    SRpiingle: 0x00
    Multiple = 0x01