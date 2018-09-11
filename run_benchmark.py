"""Run phoronix benchmarks as test-suites."""

import os

import utils

logs = "/tmp/logs"
pxenv = {'FORCE_TIMES_TO_RUN': "1",
         'SKIP_EXTERNAL_DEPENDENCIES': "1"}


def check_benchmark(b):
    """Check for new benchamrks."""
    print("\t-", check_benchmark.__name__)
    return


def phoronix_run(b):
    """Run benchmark suite."""
    print("\t-", phoronix_run.__name__)
    strace = "/usr/bin/strace -ff -o %s/%s -ttt " % (logs, b)
    pxenv.update({'EXECUTE_BINARY_PREPEND': strace})

    cmd = "phoronix-test-suite batch-benchmark local/" + b
    print("\t\t", cmd)

    rc, o, err = utils.Run(cmd, xenv=pxenv)
    if err:
        print(err, "(%s)" % rc)
    else:
        with open("%s%s.log" % (utils.results, b), "wb", 0) as f:
            cmd = "/usr/bin/strace-log-merge %s/%s" % (logs, b)
            rc, o, err = utils.Run(cmd, stdout = f)
            if rc != 0:
                print(err, "(%s)" % rc)
            os.system("rm -rf %s/*" % (logs))


def run():
    """Driver."""
    if not os.path.isdir(logs):
        os.mkdir(logs)
    if not os.path.isdir(utils.results):
        os.mkdir(utils.results)

    for benchmark in os.listdir(utils.pts):
        b = benchmark.split("-")[0]
        check_benchmark(b)
        phoronix_run(b)
