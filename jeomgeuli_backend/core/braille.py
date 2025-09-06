
import os
SIMULATE = os.environ.get("BRAILLE_SIM", "1") == "1"
SERIAL_PORT = os.environ.get("BRAILLE_PORT", "/dev/ttyUSB0")
BAUD = int(os.environ.get("BRAILLE_BAUD", "115200"))

MAP = {
    "경제":[1,1,1,1,1,1],
    "물가":[1,0,0,1,0,0],
    "정부":[1,1,0,0,0,0],
}

def to_packet(triple):
    def bits_to_byte(bits):
        val = 0
        for i,b in enumerate(bits):
            if b: val |= (1<<i)
        return val & 0x3F
    b = [bits_to_byte(x) & 0x3F for x in triple]
    chk = (b[0] ^ b[1] ^ b[2]) & 0xFF
    return bytes([0x02, b[0], b[1], b[2], chk, 0x03])

def send_keywords(keywords):
    patterns = []
    for i in range(3):
        kw = keywords[i] if i < len(keywords) else None
        patt = MAP.get(kw, [0,0,0,0,0,0])
        patterns.append(patt)
    pkt = to_packet(patterns)
    if SIMULATE:
        return {"simulate": True, "packet": list(pkt)}
    else:
        import serial
        with serial.Serial(SERIAL_PORT, BAUD, timeout=1) as ser:
            ser.write(pkt)
            ser.flush()
            line = ser.readline().decode(errors="ignore").strip()
        return {"simulate": False, "packet": list(pkt), "resp": line}
