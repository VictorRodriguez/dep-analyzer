"""Get binary and library dependencies."""

import os
import re

import utils
import json

data = {}
libraries = []
binaries = []
max_lib_cnt = 20
max_bin_cnt = 20

def get_commit(release, pkg):
    blame_log = []
    filename = "RELEASENOTES"

    url = 'https://cdn.download.clearlinux.org/releases/'+ str(release)\
        + '/clear/RELEASENOTES'
    r, o, err = utils.Run("curl " + url)
    if r != 0:
        print("NO RELSEASENOTES FOUND!! for relase: " + str(release))
        return ""

    token = "Changes in package " + (pkg)
    content = o.splitlines()
    for line in iter(content):
        if token in line:
            print(line)
            blame_log.append(line.strip())
            blame_log.append(content[content.index(line)+1].strip().\
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

    for pkg in pkgs:
        print("File : " + file_name + " is provided by : " + pkg)
    return pkg


def analysis():
    """Fill the bin/lib lists."""
    for logs in os.listdir(utils.results):
        if logs.endswith(".log"):
            log = os.path.abspath(utils.results + logs)
            benchmark = logs.split(".")[0]
            lib_count = 0
            bin_count = 0
            with open(log) as f:
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
            # TODO
            # regresion is hardcoded at this point , please let me knwo whats
            # thebest way to pass the regression version to the script
            regression = utils.get_version()
            if regression: 
                data[benchmark].append({
                    'regression': regression,
                })
            for lib in libraries:
                # print("Benchmark " + benchmark + " call: " + lib)
                pkg = whatprovides(lib)
                if (pkg):
                    data[benchmark].append({
                        'lib': lib,
                        'provided by': pkg
                    })
                    blame_log = get_commit(regression, pkg)
                    if (blame_log):
                        data[benchmark].append({
                            'changelog': blame_log,
                        })

            for binary in binaries:
                # print("Benchmark " + benchmark + " call: " + binary)
                pkg = whatprovides(binary)
                if (pkg):
                    data[benchmark].append({
                        'binary': binary,
                        'provided by': pkg
                    })
                    blame_log = get_commit(regression, pkg)
                    if (blame_log):
                        data[benchmark].append({
                            'changelog': blame_log,
                        })
            if data:
                json_file = utils.results + benchmark + "-data.json"
                with open(json_file, 'w') as outfile:
                    json.dump(data, outfile)
