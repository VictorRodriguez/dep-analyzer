#!/usr/bin/python3

import argparse
import socket

port = 5005
buffer_size = 1024


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", dest="server", action="store_true",
                        help="IP address of the dep-analyzer server (optional)")
    parser.add_argument("benchmarks",
                        help="List of pts benchmarks comma separated to extract\
                        dependencies followed by an optional CLR release version,\
                        e.g: 'pts/sqlite,pts/blogbench,local/parboil,2500'")

    args = parser.parse_args()

    if args.server:
        srv = args.server
    else:
        srv = "10.219.128.115"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connectng to: %s\nRun: %s" % (srv, args.benchmarks))
    s.connect((srv, port))

    try:
        s.sendall(bytes(args.benchmarks.encode("utf-8")))
        print("Benchmark(s) sent...")
    except e:
        print(e)


if __name__ == "__main__":
    main()
