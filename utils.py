"""Several utilities and convenient functions."""

import os
import re
import shlex
import subprocess

pts = "/var/lib/phoronix-test-suite/test-suites/local"
current_rn = 'https://cdn.download.clearlinux.org/releases/\
current/clear/RELEASENOTES'
fixed_version = 2780
results = os.getcwd() + '/results/'


def Run(command, xenv={}, check=True, **kwargs):
    """Run command."""
    rc = 1
    fullArgs = {
            "args":    shlex.split(command),
            "stdout":  subprocess.PIPE,
            "stderr":  subprocess.PIPE,
            "universal_newlines": True,
    }

    e = os.environ.copy()
    e.update(xenv)
    fullArgs['env'] = xenv

    rc = subprocess.run(**fullArgs)
    return rc.returncode, rc.stdout, rc.stderr


def get_version():
    """Get os version."""
    m = re.compile(r"Installed version: (\d+)")
    rc, o, err = Run("swupd info")
    if err == "":
        v = (m.search(o)).group(1)
        return int(v)
    else:
        m = re.compile(r"Release notes for the update from (\d+) to (\d+)")
        rc, o, err = Run("curl " + current_rn)
        if rc != 0:
            return fixed_version
        v = (m.search(o)).group(2)
        return int(v)
    return fixed_version


def update():
    """Update to the next release."""
    # get current version
    v = get_version()
    print("current version: ", v)
    return True

    # try to update to the next release
    # cmd = "swupd verify --fix --force -m " + str(v+1)
    cmd = "swupd verify --fix --force -m 9999"
    rc, o, err = Run(cmd)
    if rc != 0 or err != "":
        # no new version...time to sleep
        return False
    return True


def save_file(filename, content):
    """Append data into a file."""
    try:
        with open(filename, 'a') as f:
            f.write(content)
            f.close()
    except Exception:
        print("Error writing file '{0}'".format(filename))
        exit(1)

def write_file(filename, content):
    """Append data into a file."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
            f.close()
    except Exception:
        print("Error writing file '{0}'".format(filename))
        exit(1)
