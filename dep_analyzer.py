#!/usr/bin/python3

"""Main module."""

from analyze import analysis

from report import report_html

from run_benchmark import run


def main():
    """Run the main loop."""
    while True:
        run()
        analysis()
        report_html()


if __name__ == "__main__":
    try:
        main()
    except(KeyboardInterrupt):
        exit(0)
