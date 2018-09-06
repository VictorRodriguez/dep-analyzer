"""Run phoronix benchmarks as test-suites."""

import os

import utils

logs = "/tmp/logs"
pxenv = {'FORCE_TIMES_TO_RUN': "1",
         'SKIP_EXTERNAL_DEPENDENCIES': "1"}


def check_benchmark():
    """Check for new benchamrks."""
    print("\t-", check_benchmark.__name__)
    return


def phoronix_run():
    """Run benchmark suite."""
    print("\t-", phoronix_run.__name__)
    for t in os.listdir(utils.pts):
        e = {'EXECUTE_BINARY_PREPEND': "strace -ff -o %s/%s "
             % (logs, t.split("-")[0])}
        pxenv.update(e)
        cmd = "phoronix-test-suite batch-benchmark local/" + t
        rc, o, err = utils.Run(cmd, xenv=pxenv)
        if err:
            print(rc, err)
        else:
            os.system("cat %s/* >%s/%s.log"
                      % (logs, utils.results, t.split("-")[0]))
            os.system("rm -rf %s/*" % (logs))


def run():
    """Driver."""
    print(run.__name__)
    if not os.path.isdir(logs):
        os.mkdir(logs)
    if not os.path.isdir(utils.results):
        os.mkdir(utils.results)
    check_benchmark()
    phoronix_run()
