"""Get binary and library dependencies."""

import os
import re

import utils
import json
import wget

data = {}
libraries = []
binaries = []
yum_conf = "/etc/yum.conf"
max_lib_cnt = 20
max_bin_cnt = 20

def get_commit(release,pkg):
    blame_log = []
    # get info from :
    # https://cdn.download.clearlinux.org/releases/24660/clear/RELEASENOTES
    filename = "/tmp/RELEASENOTES-" + str(release)
    if not os.path.isfile(filename):
        url = 'https://cdn.download.clearlinux.org/releases/'+ release+'/clear/RELEASENOTES'
        filename = wget.download(url=url,out=filename)
    else:
        token = "Changes in package " + (pkg)
        with open(filename) as f:
            content = f.readlines()
            for line in content:
                if token in line:
                    print(line)
                    blame_log.append(line.strip())
                    blame_log.append(content[content.index(line)+1].strip().split("-")[0])
    tmp = list(set(blame_log))
    str1 = ''.join(tmp)
    return str1

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
    yum_log = "/tmp/yum.log"
    cmd = "dnf-3 --releasever=clear "
    cmd += " --config=/etc/dnf.conf provides "
    cmd += file_name
    # cmd += " &> /tmp/yum.log"
    r, o, err = utils.Run(cmd)
    utils.write_file(yum_log, o)
    if r == 0 or err == '':
        cmd = "repoquery -c "
        cmd += yum_conf
        cmd += " --whatprovides " + file_name
        # cmd += " &> /tmp/yum.log"
        r, o, err = utils.Run(cmd)
        if r != 0:
            #print(err)
            pass
        else:
            utils.write_file(yum_log, o)

    if os.path.isfile(yum_log):
        with open(yum_log) as f:
            content = f.readlines()
            for line in content:
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
            regression = 24760
            if regression: 
                data[benchmark].append({
                    'regresion': regression,
                })
            for lib in libraries:
                # print("Benchmark " + benchmark + " call: " + lib)
                pkg = whatprovides(lib)
                if (pkg):
                    data[benchmark].append({
                        'lib': lib,
                        'provided by': pkg
                    })
                    blame_log = get_commit(regression,pkg)
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
                    blame_log = get_commit(regression,pkg)
                    if (blame_log):
                        data[benchmark].append({
                            'changelog': blame_log,
                        })
            if data:
                json_file = "results/" + benchmark + "-data.json"
                with open(json_file, 'w') as outfile:
                    json.dump(data, outfile)
