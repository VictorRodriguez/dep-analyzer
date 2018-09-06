#!/usr/bin/env python3

"""Main module."""

import time

from analyze import analysis

from run_benchmark import run

import utils

time_to_sleep = 360  # ~1hr


def main():
    """Run the main loop."""
    while True:
        if utils.update():
            run()
            analysis()
            # report()
        time.sleep(time_to_sleep)


if __name__ == "__main__":
    try:
        main()
    except(KeyboardInterrupt):
        exit(0)
