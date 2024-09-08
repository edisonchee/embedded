import serial
import wave
import struct

# Serial port configuration
PORT = 'COM4'  # Change this to your serial port
BAUD_RATE = 115200  # Change this to your baud rate
CHUNK_SIZE = 1024 # Number of bytes to read at a time
TIMEOUT = 1

# WAV file configuration
SAMPLE_RATE = 16000  # Change this to your desired sample rate
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit

def main():
    # Open serial port
    ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {PORT}")

    # Kill inferencer
    ser.write('b'.encode('utf-8'))
    while True: 
        data = ser.readline()
        if data: break

    # Open WAV file for writing
    with wave.open('output.wav', 'wb') as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)

        try:
            while True:
                # Read data from serial port
                data = ser.read(CHUNK_SIZE)  # Read 1024 bytes at a time
                if not data:
                    break

                # 16-bit signed PCM samples (big endian)
                samples = struct.unpack(f'>{len(data)//2}h', data)
                # convert to little endian
                wav_file.writeframes(struct.pack(f'<{len(samples)}h', *samples))

        except KeyboardInterrupt:
            print("Recording stopped")

        finally:
            ser.close()
            print("Serial port closed")

main()
