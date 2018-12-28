#!/usr/bin/env python3
import sys
import logging
import argparse
import asyncio
import pyeverlights

RED = 16711680
GREEN = 65280
BLUE = 255
WHITE = 0xffffff

parser = argparse.ArgumentParser("Control an EverLights lighting system.")
parser.add_argument('--ip', required=True)
parser.add_argument('-v', '--verbose',
                    action='store_const', const=logging.DEBUG, default=logging.WARN)

args = parser.parse_args()
logging.basicConfig(level=args.verbose)

async def main():
  el = pyeverlights.EverLights(args.ip)

  await el.get_status()

  #await el.set_pattern(1, [WHITE, RED, GREEN, BLUE], {pyeverlights.MODE_CHASE: 64})
  colors = await el.set_pattern_by_id(1, "Xmas")
  print(colors[0])

  await el.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print("Done")
