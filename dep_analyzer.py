#!/usr/bin/env python3

"""Main module."""

from time import sleep

from analyze import analysis

from run_benchmark import run

from report import report_html

from utils import update

time_to_sleep = 360  # ~1hr


def main():
    """Run the main loop."""
    while True:
        if update():
            run()
            analysis()
            report_html()
            print("waiting for next build...")
        sleep(time_to_sleep)


if __name__ == "__main__":
    try:
        main()
    except(KeyboardInterrupt):
        exit(0)
