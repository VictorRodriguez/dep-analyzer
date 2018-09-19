"""Several utilities and convenient functions."""

import os
import re
import shlex
import subprocess

pts = "/var/lib/phoronix-test-suite/test-suites/local"
current_rn = 'https://cdn.download.clearlinux.org/releases/\
current/clear/RELEASENOTES'
fixed_version = "2780"
results = os.getcwd() + '/results/'
regression = ""


def Run(command, xenv={}, check=True, **kwargs):
    """Run command."""
    rc = 1
    fullArgs = {
            "args":    shlex.split(command),
            "stdout":  subprocess.PIPE,
            "stderr":  subprocess.PIPE,
            "universal_newlines": True,
    }

    if xenv:
        e = os.environ.copy()
        e.update(xenv)
        fullArgs['env'] = xenv

    fullArgs.update(kwargs)

    rc = subprocess.run(**fullArgs)
    return rc.returncode, rc.stdout, rc.stderr


def get_version():
    """Get os version."""
    m = re.compile(r"Installed version: (\d+)")
    rc, o, err = Run("swupd info")
    if err == "":
        v = (m.search(o)).group(1)
        return v
    else:
        m = re.compile(r"Release notes for the update from (\d+) to (\d+)")
        rc, o, err = Run("curl " + current_rn)
        if rc != 0:
            return fixed_version
        v = (m.search(o)).group(2)
        return v
    return fixed_version


def update():
    """Update to the next release."""
    global regression
    # try to update to the next release
    print("\tupdating to " + regression)
    cmd = "swupd verify --fix --force -m " + regression
    rc, o, err = Run(cmd)
    if rc != 0 or err != "":
        regression = get_version()
    return


def save_file(filename, content):
    """Append data into a file."""
    try:
        with open(filename, 'a') as f:
            f.write(content)
    except Exception:
        print("Error writing file '{0}'".format(filename))
        exit(1)


def write_file(filename, content):
    """Append data into a file."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
    except Exception:
        print("Error writing file '{0}'".format(filename))
        exit(1)
