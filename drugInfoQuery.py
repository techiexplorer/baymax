from flask import Flask
from flask import request

from dbAnalysis import create_drug_data

drugApp = Flask(__name__)


@drugApp.route('/')
def get_base_schema():
    return "Hello, welcome to Baymax"


@drugApp.route('/idVsCommonName')
def load_drug_id_vs_common_name():
    return create_drug_data()[0]


@drugApp.route('/commonNameVsNames')
def load_common_name_vs_synonyms():
    drug_name = request.args.get('drug_name', default=None, type=str)
    if drug_name:
        try:
            return str(create_drug_data()[1][drug_name])
        except Exception:
            return "Drug not found"
    else:
        return create_drug_data()[1]


@drugApp.route('/searchDrug')
def search_drug():
    search_drug_name = request.args.get('search_drug_name', default=None, type=str)
    if search_drug_name:
        new_dict = create_drug_data()[1]
        x = ""
        for k, v in new_dict.items():
            print(k, v)
            if search_drug_name in str(v):
                return k + ": " + str(new_dict[k])
                # break
        # return str(x)
    else:
        return create_drug_data()[1]


drugApp.run()
