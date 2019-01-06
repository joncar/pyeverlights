# pyeverlights

This project provides a simple Python3 module for interfacing with an [EverLights](http://myeverlights.com/) control box.

## Example
```
import pyeverlights
import asyncio

async def main():
  el = pyeverlights.EverLights("10.0.0.100")

  # Set zone 1 to solid red
  await el.set_pattern(pyeverlights.ZONE_1, [0xff0000])

  # Set zone 1 to saved pattern "Testing"
  await el.set_pattern_by_id(args.zone, "Testing")

  # Get control box status
  await el.get_status()

  await el.close()
  
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
