import serial, time, csv

ser = serial.Serial('COM3', 115200)

data_to_be_written = list()

time_end = time.time() + 180
while time.time() < time_end:
  data = ser.readline()
  data_to_be_written.append(data.decode('utf-8').strip())

with open('data.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(['accel_x', 'accel_y', 'accel_z'])
  for data in data_to_be_written:
    writer.writerow(data.split(','))

print("Goodbye world")