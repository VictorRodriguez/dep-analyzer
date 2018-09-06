import os
import re

import utils

data = {}
libraries = []
binaries = []
yum_conf = "/etc/yum.conf"

def add_binary(binary):
    if os.path.isfile(binary):
        if binary not in binaries:
            binaries.append(binary)

def add_lib(lib):
    if os.path.isfile(lib):
        if lib not in libraries:
            libraries.append(lib)

def whatprovides(file_name):
    pkgs = []
    pkg = ""
    yum_log = "/tmp/yum.log"
    cmd = "dnf-3 --releasever=clear "
    cmd += " --config=/etc/dnf.conf provides "
    cmd += file_name
    # cmd += " &> /tmp/yum.log"
    r, o, err = utils.Run(cmd)
    utils.save_file(yum_log, o)
    if r == 0 or err == '':
        cmd = "repoquery -c "
        cmd += yum_conf
        cmd += " --whatprovides " + file_name
        # cmd += " &> /tmp/yum.log"
        r, o, err = utils.Run(cmd)
        if r != 0:
            print(err)
        else:
            utils.save_file(yum_log, o)

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
    for logs in os.listdir(utils.results):
        l = os.path.abspath(utils.results + logs)
        benchmark = logs.split(".")[0]
        lib_count = 0
        bin_count = 0
        with open(l) as f:
            content = f.readlines()
            for line in content:
                if "openat" in line or "access" in line:
                    if "/usr/lib" in line and lib_count < 10:
                        m = re.search('<(.+?)>', line)
                        if m:
                            lib = m.group(1)
                            add_lib(lib)
                            lib_count +=1
                    if "/usr/bin" in line and bin_count < 10:
                        m = re.search('/usr/bin/(.+?)"',line)
                        if m:
                            binary = "/usr/bin/" + m.group(1)
                            add_binary(binary)
                            bin_count +=1

        data[benchmark] = []
        for lib in libraries:
            print("Benchmark " + benchmark + " call: " + lib)
            pkg = whatprovides(lib)
            if (pkg):
                data[benchmark].append({
                    'lib': lib,
                    'provided by': pkg
                })

        for binary in binaries:
            print("Benchmark " + benchmark + " call: " + binary)
            pkg = whatprovides(binary)
            if (pkg):
                data[benchmark].append({
                    'binary': binary,
                    'provided by': pkg
                })

        # if "strace" not in data[benchmark]:
        #     strace_log = benchmark.replace("/","-") + "-strace.log"
        #     data[benchmark].append({
        #             'strace':strace_log
        #             })
        # if data:
        #     merge_dict = {}
        #     if os.path.isfile('data.json'):
        #         if data_json_valid:
        #             with open('data.json') as json_file:
        #                 data_json = json.load(json_file)
        #                 if data_json:
        #                     merge_dict = {**data, **data_json}
        #     if not merge_dict:
        #         merge_dict = data
        #     with open('data.json', 'w') as outfile:
        #         json.dump(merge_dict, outfile)

