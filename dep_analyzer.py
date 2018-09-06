#!/usr/bin/env python3

import time

from run_benchmark import run
from analyze import analysis
import utils

time_to_sleep = 360 # 1hr

def main():
   while True:
      if utils.update():
         run()
         # analysis()
         # report()
      time.sleep(time_to_sleep)

if __name__ == "__main__":
   try:
      main()
   except(KeyboardInterrupt):
      exit(0)
