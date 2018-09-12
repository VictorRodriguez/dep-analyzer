"""Print HTML report."""
import json
import os

from jinja2 import Environment, FileSystemLoader

import utils


def print_html_doc(dictionary_data):
    """Generate the html index."""
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print(j2_env.get_template('test_template.html').
          render(data=dictionary_data),
          file=open("%sindex.html" % (utils.results), "w"))


def merge_report():
    """Merge all benchmakr dependencies."""
    merged_json = {}
    for f in os.listdir(utils.results):
        if f.endswith(".json"):
            f = os.path.abspath(utils.results + f)
            with open(f) as jf:
                jsonl = json.load(jf)
            if jsonl:
                merged_json.update(**jsonl)
    with open("%sdata.json" % (utils.results), 'w') as outfile:
        json.dump(merged_json, outfile)


def report_html():
    """Create the report."""
    data_json = merge_report()
    with open("%sdata.json" % (utils.results), 'r') as json_file:
        data_json = json.load(json_file)
        print_html_doc(data_json)
        print("index.html generated")
    utils.Run("rm %sdata.json" % (utils.results))
