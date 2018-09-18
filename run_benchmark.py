"""Run phoronix benchmarks as test-suites."""

import os

import utils

import socket

logs = "/tmp/logs"
pxenv = {'FORCE_TIMES_TO_RUN': "1",
         'SKIP_EXTERNAL_DEPENDENCIES': "1"}
ip_address = '127.0.0.1'
port =       5005
buffer_size= 1024


def get_benchmarks():
    """Check for new benchamrks."""
    print(" :", get_benchmarks.__name__)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_address, port))
    s.listen(1)

    conn, addr = s.accept()
    data = str(conn.recv(buffer_size), 'utf-8')
    conn.close()

    return data


def phoronix_install(b):
    """Install benchamrks."""
    print(" :", phoronix_install.__name__)

    for i in b:
        cmd = "phoronix-test-suite force-install " + i
        print("\t", cmd)

        rc, o, err = utils.Run(cmd)
        if err:
            print(err, "(%s)" % rc)


def phoronix_run(benchmark):
    """Run benchmark suite."""
    print(" :", phoronix_run.__name__)

    for b in benchmark:
        b = b.split("/")[1]
        strace = "/usr/bin/strace -ff -o %s/%s -ttt " % (logs, b)
        pxenv.update({'EXECUTE_BINARY_PREPEND': strace})

        cmd = "phoronix-test-suite batch-run " + b
        print("\t", cmd)

        rc, o, err = utils.Run(cmd, xenv=pxenv)
        if err:
            print(err, "(%s)" % rc)
        else:
            with open("%s%s.log" % (utils.results, b), "wb", 0) as f:
                cmd = "/usr/bin/strace-log-merge %s/%s" % (logs, b)
                rc, o, err = utils.Run(cmd, stdout=f)
                if rc != 0:
                    print(err, "(%s)" % rc)


def run():
    """Driver."""
    print("-", run.__name__)
    if not os.path.isdir(logs):
        os.mkdir(logs)
    if not os.path.isdir(utils.results):
        os.mkdir(utils.results)
    os.system("rm -rf %s/* %s*" % (logs, utils.results))

    benchmark = get_benchmarks().split(",")
    regression = benchmark.pop()
    phoronix_install(benchmark)
    phoronix_run(benchmark)
