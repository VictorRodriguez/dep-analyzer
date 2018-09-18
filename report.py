"""Print HTML report."""
import json
import os

from jinja2 import Environment, FileSystemLoader

import utils

report_page = '/var/www/html/dep-analyzer/'

def print_html_doc(dictionary_data):
    """Generate the html index."""
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print(j2_env.get_template('test_template.html').
          render(data=dictionary_data),
          file=open("%sindex.html" % (report_page), "w"))


def report_html():
    """Create the report."""
    print("-", report_html.__name__)
    with open("%sdata.json" % (utils.results), 'r') as json_file:
        data_json = json.load(json_file)
        print_html_doc(data_json)
        print(" : index.html generated")
    utils.Run("rm %sdata.json" % (utils.results))
