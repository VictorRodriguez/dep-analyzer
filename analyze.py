"""Get binary and library dependencies."""

import json
import os
import re

import utils


data = {}
libraries = []
binaries = []
max_lib_cnt = 20
max_bin_cnt = 20
release_notes = ""


def get_release_notes(regression):
    """Get the release notes."""
    global release_notes

    url = 'https://cdn.download.clearlinux.org/releases/'+ regression\
        + '/clear/RELEASENOTES'

    r, release_notes, err = utils.Run("curl " + url)
    if r != 0:
        print("NO RELSEASENOTES FOUND!! for relase: " + regression)
        return ""


def get_commit(pkg):
    """Get blame info."""
    blame_log = []

    token = "Changes in package " + (pkg)
    content = release_notes.splitlines()
    for line in iter(content):
        if token in line:
            print("\t" + line)
            blame_log.append(line.strip())
            blame_log.append(content[content.index(line)+1].strip().
                             split("-")[0])
    tmp = list(set(blame_log))
    return ''.join(tmp)


def add_binary(binary):
    """Add a binary to the list."""
    if os.path.isfile(binary):
        if binary not in binaries:
            binaries.append(binary)


def add_lib(lib):
    """Add a library to the list."""
    if os.path.isfile(lib):
        if lib not in libraries:
            libraries.append(lib)


def whatprovides(file_name):
    """Get the bundle that  provides a file name."""
    pkgs = []
    pkg = ""

    cmd = "repoquery -c /etc/yum.conf  --whatprovides " + file_name
    r, o, err = utils.Run(cmd)
    if r != 0:
        cmd = "dnf-3 --releasever=clear  --config=/etc/dnf.conf provides "
        cmd += file_name
        r, o, err = utils.Run(cmd)
        if r != 0:
            return pkgs

    for line in iter(o.splitlines()):
        if ".x86_64" in line:
            pkg = line.split("-")[0]
            if pkg not in pkgs:
                pkgs.append(pkg)

    # for pkg in pkgs:
    #     print("\tFile : " + file_name + " is provided by : " + pkg)
    return pkg


def analysis():
    """Fill the bin/lib lists."""
    print("-", analysis.__name__)

    get_release_notes(utils.regression)

    for logs in os.listdir(utils.results):
        if logs.endswith(".log"):
            log = os.path.abspath(utils.results + logs)
            benchmark = logs.split(".")[0]
            lib_count = 0
            bin_count = 0
            with open(log, "r") as f:
                print(" : extract dependencies from", benchmark)
                content = f.readlines()
                for line in content:
                    if "openat" in line or "access" in line:
                        if "/usr/lib" in line and lib_count < max_lib_cnt:
                            m = re.search('<(.+?)>', line)
                            if m:
                                lib = m.group(1)
                                add_lib(lib)
                                lib_count += 1
                        if "/usr/bin" in line and bin_count < max_bin_cnt:
                            m = re.search('/usr/bin/(.+?)"', line)
                            if m:
                                binary = "/usr/bin/" + m.group(1)
                                add_binary(binary)
                                bin_count += 1

            data[benchmark] = []
            if utils.regression:
                data[benchmark].append({
                    'regression': utils.regression,
                })
            for lib in libraries:
                pkg = whatprovides(lib)
                if (pkg):
                    data[benchmark].append({
                        'lib': lib,
                        'provided by': pkg
                    })
                    blame_log = get_commit(pkg)
                    if (blame_log):
                        data[benchmark].append({
                            'changelog': blame_log,
                        })

            for binary in binaries:
                pkg = whatprovides(binary)
                if (pkg):
                    data[benchmark].append({
                        'binary': binary,
                        'provided by': pkg
                    })
                    blame_log = get_commit(pkg)
                    if (blame_log):
                        data[benchmark].append({
                            'changelog': blame_log,
                        })

    libraries.clear()
    binaries.clear()

    if data:
        json_file = utils.results + "data.json"
        with open(json_file, 'w') as outfile:
            json.dump(data, outfile)
        data.clear()
