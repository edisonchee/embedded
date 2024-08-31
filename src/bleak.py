import time, asyncio, struct, csv
from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

BLE_DEVICE_ADDRESS = ""
data_to_be_written = list()

async def run_ble_client(queue: asyncio.Queue):
  # devices = await BleakScanner.discover()
  # for d in devices:
  #   print(d)
  device = await BleakScanner.find_device_by_address(BLE_DEVICE_ADDRESS)
  
  async def notification_cb_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    await queue.put((time.time_ns(), data))
    
  async with BleakClient(device) as client:
    if client.is_connected:
      print(f"Connected: {client.is_connected}")
      print(f"Size: {client.mtu_size}")
    services = await client.get_services()
    for s in services:
      print(f'{s.uuid} {s.handle} {s.description}')
      if s.handle == 10:
        for c in s.characteristics:
          print(f'{c.uuid}')
          await client.start_notify(c, notification_cb_handler)
          await asyncio.sleep(5.0)
          await client.stop_notify(c)
          await queue.put((time.time(), None))
          print(f'\n')
  
  print(f"Client is disconnected: {client.is_connected}")

async def run_queue_consumer(queue: asyncio.Queue):
  while True:
    timestamp, data = await queue.get()
    if data is None:
      print(f"Timestamp: {timestamp}, No data")
      return
    else:
      data_to_be_written.append([timestamp] + unpack_data(data))
    queue.task_done()

def unpack_data(data: bytearray):
  data_list = list()
  for i in range(0, len(data), 4):
    data_list.append(struct.unpack('f', data[i:i+4])[0])
  return data_list

async def main():
  queue = asyncio.Queue()
  client_task = await run_ble_client(queue)
  consumer_task = await run_queue_consumer(queue)

  try:
    await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
    write_to_csv()
  except KeyboardInterrupt:
    print("Exiting...")
    client_task.cancel()
    consumer_task.cancel()
    await asyncio.gather(client_task, consumer_task, return_exceptions=True)
    exit(1)

  exit(0)

def write_to_csv():
  with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'accel_x', 'accel_y', 'accel_z'])
    for data in data_to_be_written:
      data[0] = data[0] / 1000000 # Convert nanoseconds to milliseconds
      writer.writerow(data)

asyncio.run(main())
