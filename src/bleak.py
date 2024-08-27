import time, asyncio, struct
from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

BLE_DEVICE_ADDRESS = ""

async def run_ble_client(queue: asyncio.Queue):
  # devices = await BleakScanner.discover()
  # for d in devices:
  #   print(d)
  device = await BleakScanner.find_device_by_address(BLE_DEVICE_ADDRESS)
  
  async def notification_cb_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    await queue.put((time.time(), data))
    
  async with BleakClient(device) as client:
    if client.is_connected:
      print(f"Connected: {client.is_connected}")
      print(f"Size: {client.mtu_size}")
    services = await client.get_services()
    for s in services:
      print(f'{s.uuid} {s.handle} {s.description}')
      if s.handle == 10:
        for c in s.characteristics:
          if c.handle == 19 or c.handle == 22 or c.handle == 25:
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
    else:
      print(f"Timestamp: {timestamp}, Data: {data}, {struct.unpack('f', data[0:4])}")
    queue.task_done()

async def main():
  queue = asyncio.Queue()
  client_task = run_ble_client(queue)
  consumer_task = run_queue_consumer(queue)

  try:
    await asyncio.gather(client_task, consumer_task)
  except KeyboardInterrupt:
    print("Exiting...")
    client_task.cancel()
    consumer_task.cancel()
    await asyncio.gather(client_task, consumer_task, return_exceptions=True)
    exit(1)

  exit(0)

asyncio.run(main())
