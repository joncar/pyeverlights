#!/usr/bin/env python3
import sys
import logging
import argparse
import asyncio
import json
import pyeverlights

async def cmd_status():
  print(json.dumps(await el.get_status(), sort_keys=True, indent=4))

async def cmd_color():
  await el.set_pattern(args.zone, [args.red*0x10000+args.green*0x100+args.blue])

async def cmd_pattern():
  await el.set_pattern_by_id(args.zone, args.pattern)

def parse_args():
  parser = argparse.ArgumentParser("Control an EverLights lighting system.")
  parser.add_argument('--ip', required=True)
  parser.add_argument('-v', '--verbose',
                      action='store_const', const=logging.DEBUG, default=logging.WARN)

  subparsers = parser.add_subparsers()

  parser_status = subparsers.add_parser('status', help='Get control box status.')
  parser_status.set_defaults(func=cmd_status)

  parser_color = subparsers.add_parser('color', help='Set all lights to a single color.')
  parser_color.add_argument('red', type=int)
  parser_color.add_argument('green', type=int)
  parser_color.add_argument('blue', type=int)
  parser_color.add_argument('--zone', default=pyeverlights.ZONE_1)
  parser_color.set_defaults(func=cmd_color)

  parser_pattern = subparsers.add_parser('pattern', help='Start a saved pattern.')
  parser_pattern.add_argument('pattern')
  parser_pattern.add_argument('--zone', default=pyeverlights.ZONE_1)
  parser_pattern.set_defaults(func=cmd_pattern)

  return parser.parse_args()

async def main():
  global el, args
  args = parse_args()
  logging.basicConfig(level=args.verbose)
  el = pyeverlights.EverLights(args.ip)
  await args.func()
  await el.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print("Done")
