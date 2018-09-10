"""Print HTML report"""
import os
import utils
import json
from jinja2 import Environment, FileSystemLoader

def print_html_doc(dictionary_data):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print(j2_env.get_template('test_template.html').render(data=dictionary_data),file=open("index.html","w"))

def report_html():
    for f in os.listdir(utils.results):
        if f.endswith(".json"):
            f = os.path.abspath(utils.results + f)
            print(f)
            with open(f) as json_file:
                data_json = json.load(json_file)
                print_html_doc(data_json)
            print("index.html generated")
        if os.path.isfile("index.html"):
            newpath = r'results'
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                os.system('mv index.html results/index.html')
            else:
                os.system('mv index.html results/index.html')

