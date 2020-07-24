import matplotlib.pylab as pyl
import sounddevice as sd

# bits to send
bits = [1, 0, 1, 1, 0, 0, 0, 1]
# time between samples
sampling_period = 0.0000226758
# Time period
ts = pyl.arange(0, 8, sampling_period)
# Carrier Frecuency
fc = 800

def get_4PAM_modulation(ts, fc, bits):
    lenghtBits = len(bits)
    lenghtChunk = 2 * len(ts)//lenghtBits    # Chunks now are double sized
    A = []  # Amplitudes
    currentBit = 0
    while (currentBit < lenghtBits):
        oneBit = bits[currentBit]
        currentBit += 1
        anotherBit = bits[currentBit]
        currentBit += 1
        for j in range(lenghtChunk):
            A_for_current_bits = 0
            if (oneBit == 0 and anotherBit == 0):   # 00
                A_for_current_bits = 0
            elif (oneBit == 0 and anotherBit == 1): # 01
                A_for_current_bits = 0.5
            elif (oneBit == 1 and anotherBit == 0): # 10
                A_for_current_bits = 2
            else:                                   # 11
                A_for_current_bits = 4
            A.append(A_for_current_bits)
    return A * pyl.sin(2.0 * pyl.pi * fc * ts)

def getOOKModulation(ts, fc, bits):
    lenghtBits = len(bits)
    lenghtChunk = int(len(ts)/lenghtBits)
    A = []
    for i in range(lenghtBits):
        for j in range(lenghtChunk):
            A_for_Bit_i = bits[i]
            A.append(A_for_Bit_i)
    return A * pyl.sin(2.0 * pyl.pi * fc * ts)

def customModulation(ts, fc, bits):
    # this custom ASK modulation (amplitude-shift modulation) is for support
    # for CDMA, in this case: 0, -2, 2. Each number will have certain amplitude
    lenghtBits = len(bits)
    lenghtChunk = int(len(ts)/lenghtBits)
    A = []
    for i in range(lenghtBits):
        for j in range(lenghtChunk):
            A_for_Bit_i = 0
            if (bits[i] == 0):
                A_for_Bit_i = 0
            elif (bits[i] == 2):
                A_for_Bit_i = 4
            elif (bits[i] == -2):
                A_for_Bit_i = 2
            A.append(A_for_Bit_i)
    return A * pyl.sin(2.0 * pyl.pi * fc * ts)

ym = getOOKModulation(ts, fc, bits)
y_paso2 = get_4PAM_modulation(ts, fc, bits)

#TODO: Need to transmit signal with sound
fs = 44100
sd.play(y_paso2, fs, blocking=True)

# Plotting results
pyl.plot(ts, y_paso2)
pyl.xlabel("tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.title("Senal enviada por transmisor")
pyl.show()